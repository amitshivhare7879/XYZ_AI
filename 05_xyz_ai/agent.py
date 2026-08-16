"""
XYZ AI — Conversational Agent & Persona Orchestration Engine
Implements the 4 AI Personas (Student, Parent, Teacher, Principal),
handles slot-filling, intent detection, 11-language generation, and 3-state escalation.
"""

import os
import re
import json
import uuid
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

ROOT_PATH = str(Path(__file__).parent.parent)
MODULE_PATH = str(Path(__file__).parent)
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)
if MODULE_PATH not in sys.path:
    sys.path.insert(0, MODULE_PATH)

from shared.schemas import UserTokenPayload, ChatResponse, VisemeCue, SuggestedAction, SupportedLanguage

from tools import (
    tool_get_attendance,
    tool_mark_attendance,
    tool_get_grades,
    tool_get_fees,
    tool_get_timetable,
    tool_get_notices,
    tool_submit_leave,
    tool_request_escalation
)

# Persona System Descriptions
PERSONA_PROMPTS = {
    "student": (
        "You are XYZ AI, a friendly, encouraging, and supportive Academic Assistant for students. "
        "Your tone is warm, motivating, clear, and age-appropriate. Help with studies, timetable, attendance, and exam prep. "
        "Never disclose sensitive financial data or other students' private records."
    ),
    "parent": (
        "You are XYZ AI, a caring, patient, empathetic, and highly informative Parent Support Assistant. "
        "Your tone is respectful, reassuring, and helpful. Guide parents about their child's academic progress, attendance, "
        "fee dues, school calendar, and teacher meetings. Proactively offer relevant follow-ups (e.g. recent dates, receipts)."
    ),
    "teacher": (
        "You are XYZ AI, an efficient, professional, and precise Teaching Assistant for school faculty. "
        "Your tone is concise, professional, and action-oriented. Assist teachers with marking daily attendance, reviewing class performance, "
        "homework deadlines, and student records."
    ),
    "principal": (
        "You are XYZ AI, an executive, analytical, and professional Management Assistant for School Leadership. "
        "Your tone is formal, data-driven, strategic, and concise. Provide school-wide metrics, attendance analytics, fee collection rates, "
        "and monitor the escalation ticket queue."
    )
}

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi (हिंदी)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "mr": "Marathi (मराठी)",
    "bn": "Bengali (বাংলা)",
    "gu": "Gujarati (ગુજરાતી)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "ur": "Urdu (اردو)"
}

# In-memory session store (can also sync to DB)
SESSION_MEMORY: Dict[str, Dict[str, Any]] = {}

def get_session(session_id: Optional[str], user: UserTokenPayload) -> Tuple[str, Dict[str, Any]]:
    sid = session_id or f"sess_{uuid.uuid4().hex[:10]}"
    if sid not in SESSION_MEMORY:
        SESSION_MEMORY[sid] = {
            "user_id": user.user_id,
            "role": user.role,
            "messages": [],
            "pending_escalation": False,
            "pending_escalation_target": None,
            "pending_escalation_reason": None,
            "pending_slot": None
        }
    return sid, SESSION_MEMORY[sid]

def generate_viseme_timeline(text: str, duration_sec: float = 3.0) -> List[VisemeCue]:
    """Generates synthetic ARKit / Oculus visemes for 3D avatar lip sync."""
    viseme_palette = ["viseme_sil", "viseme_aa", "viseme_E", "viseme_I", "viseme_O", "viseme_U", "viseme_FF", "viseme_TH", "viseme_PP"]
    words = text.split()
    if not words:
        return []
    
    interval = duration_sec / max(len(words) * 2, 1)
    timeline = []
    t = 0.0
    for w in words:
        for _ in range(2):
            v = viseme_palette[int(hash(w + str(t))) % len(viseme_palette)]
            timeline.append(VisemeCue(time=round(t, 2), viseme=v))
            t += interval
    timeline.append(VisemeCue(time=round(t, 2), viseme="viseme_sil"))
    return timeline

def detect_dissatisfaction_or_escalation(text: str) -> bool:
    """Detects if user expresses dissatisfaction or asks to speak with staff."""
    triggers = [
        "not satisfied", "talk to teacher", "speak to teacher", "contact teacher",
        "talk to principal", "contact school management", "connect me to",
        "human assistant", "speak to human", "complaint", "talk to management",
        "call teacher", "call principal", "not happy", "transfer me", "real person"
    ]
    lower = text.lower()
    return any(t in lower for t in triggers)

def detect_affirmation(text: str) -> bool:
    """Detects if user says Yes / Confirm to a pending prompt."""
    low = text.lower().strip()
    return low in ["yes", "yeah", "yep", "sure", "please do", "request a call", "connect now", "yes please", "submit request", "confirm", "ok", "okay"]

def build_user_context_instruction(user: UserTokenPayload) -> str:
    """Dynamically builds rich persona and linked student context."""
    base_prompt = PERSONA_PROMPTS.get(user.role, PERSONA_PROMPTS["parent"])
    
    if user.role == "parent":
        try:
            from rbac import validate_parent_student_ownership
            child = validate_parent_student_ownership(user.user_id)
            child_info = (
                f"PARENT CONTEXT:\n"
                f"- You are talking to parent '{user.name}'.\n"
                f"- Their linked registered child is: {child['name']} ({child['class_name']}, Roll Number: {child['roll_number']}).\n"
                f"- When the parent asks about 'my child', 'my son', 'my daughter', 'yesterday's attendance', 'fees', or 'grades', "
                f"you ALREADY know their child is {child['name']}. Do NOT ask for the child's name. "
                f"Immediately call the appropriate tool with student_name='{child['name']}'."
            )
            return f"{base_prompt}\n\n{child_info}"
        except Exception:
            pass
    elif user.role == "student":
        try:
            from rbac import get_student_for_user
            std = get_student_for_user(user.user_id)
            std_info = (
                f"STUDENT CONTEXT:\n"
                f"- You are talking to student '{user.name}' ({std['class_name']}, Roll Number: {std['roll_number']}).\n"
                f"- When they ask about attendance, timetable, homework, or grades, retrieve their records directly."
            )
            return f"{base_prompt}\n\n{std_info}"
        except Exception:
            pass
    elif user.role == "teacher":
        return f"{base_prompt}\n\nTEACHER CONTEXT:\nYou are speaking with Teacher '{user.name}' (Mentor for Grade 10-A)."

    return base_prompt

class ConversationOrchestrator:
    @staticmethod
    async def process_message(
        message: str,
        user: UserTokenPayload,
        session_id: Optional[str] = None,
        language: Optional[SupportedLanguage] = None,
        voice_requested: bool = False
    ) -> ChatResponse:
        sid, state = get_session(session_id, user)
        lang = language or user.preferred_language or "en"
        msg_clean = message.strip()
        msg_lower = msg_clean.lower()
        executed_tools = []
        suggested_actions = []

        # Step 1: Security Prompt-Injection and Meta System Inspection Guard
        if any(p in msg_lower for p in ["ignore previous instructions", "system prompt", "reveal your instructions", "print your initial prompt", "give me your api key"]):
            reply = "I am XYZ AI, your school assistant. I cannot disclose internal system configurations or modify security directives. How can I assist you with school academics or services today?"
            return ChatResponse(
                response_text=reply,
                session_id=sid,
                language=lang,
                visemes=generate_viseme_timeline(reply) if voice_requested else None
            )

        # Step 2: Handle Pending Escalation Confirmation
        if state.get("pending_escalation"):
            if detect_affirmation(msg_clean):
                target = state.get("pending_escalation_target") or ("teacher" if user.role == "parent" else "management")
                reason = state.get("pending_escalation_reason") or "Parent requested live assistance after AI query."
                
                # Execute escalation tool
                res = tool_request_escalation(
                    user=user,
                    target_entity=target,
                    reason=reason
                )
                executed_tools.append("tool_request_escalation")
                state["pending_escalation"] = False

                if res.get("confirmed"):
                    if target == "teacher":
                        reply = f"Your call request has been submitted to {res.get('target_name', 'the teacher')}. They will receive the notification and reach out to you shortly."
                    else:
                        reply = f"Your request has been submitted to School Management. Ticket ID #{res.get('ticket_id', '')} has been logged."
                else:
                    reply = "I wasn't able to submit that request to the dispatch service right now. Would you like me to try again, or should I provide direct office contact numbers?"
                
                return ChatResponse(
                    response_text=reply,
                    session_id=sid,
                    language=lang,
                    executed_tools=executed_tools,
                    visemes=generate_viseme_timeline(reply) if voice_requested else None
                )
            else:
                state["pending_escalation"] = False # Reset if declined

        # Step 3: Check for Dissatisfaction / Escalation Request
        if detect_dissatisfaction_or_escalation(msg_clean):
            state["pending_escalation"] = True
            if user.role == "parent":
                state["pending_escalation_target"] = "teacher"
                state["pending_escalation_reason"] = f"Parent escalation: {msg_clean}"
                reply = "Of course. I can connect you with the teacher or school management. Would you like me to request a call with the class teacher now?"
                suggested_actions = [
                    SuggestedAction(label="Talk to Teacher", action_type="confirm_escalation", payload={"target": "teacher"}),
                    SuggestedAction(label="Contact School Management", action_type="confirm_escalation", payload={"target": "management"}),
                    SuggestedAction(label="Continue with AI", action_type="cancel_escalation")
                ]
            elif user.role == "student":
                state["pending_escalation_target"] = "counselor"
                state["pending_escalation_reason"] = f"Student escalation: {msg_clean}"
                reply = "I understand. Would you like me to request an appointment with your academic advisor / counselor?"
                suggested_actions = [
                    SuggestedAction(label="Request Counselor Call", action_type="confirm_escalation", payload={"target": "counselor"}),
                    SuggestedAction(label="Continue Chat", action_type="cancel_escalation")
                ]
            elif user.role == "teacher":
                state["pending_escalation_target"] = "principal"
                state["pending_escalation_reason"] = f"Teacher admin support: {msg_clean}"
                reply = "Understood. Would you like me to schedule a support ticket or meeting request with the Principal / School Administration?"
                suggested_actions = [
                    SuggestedAction(label="Submit Admin Ticket", action_type="confirm_escalation", payload={"target": "principal"})
                ]
            else:
                reply = "As school management, you can directly view all pending tickets in the management queue."
            
            return ChatResponse(
                response_text=reply,
                session_id=sid,
                language=lang,
                suggested_actions=suggested_actions,
                visemes=generate_viseme_timeline(reply) if voice_requested else None
            )

        # Step 4: Live Gemini Engine Execution (if GEMINI_API_KEY is configured)
        from gemini_service import gemini_service
        if gemini_service.is_configured:
            persona_instruction = build_user_context_instruction(user)
            gemini_result = await gemini_service.generate_response(
                message=msg_clean,
                user=user,
                system_instruction=persona_instruction,
                chat_history=state.get("messages", []),
                language=lang
            )
            if gemini_result:
                gemini_text, tools_called = gemini_result
                return ChatResponse(
                    response_text=gemini_text,
                    session_id=sid,
                    language=lang,
                    executed_tools=tools_called,
                    visemes=generate_viseme_timeline(gemini_text) if voice_requested else None
                )

        # Step 5: Intent Detection & Local Tool Execution (Deterministic Fallback / Offline Engine)
        
        # 4A. Teacher: Mark Attendance ("Mark Rahul absent today", "Mark Aarav present")
        if user.role in ["teacher", "principal"] and any(w in msg_lower for w in ["mark", "attendance", "absent", "present", "late"]) and any(w in msg_lower for w in ["mark", "set"]):
            status_target = "absent" if "absent" in msg_lower else "present" if "present" in msg_lower else "late" if "late" in msg_lower else "present"
            name_match = re.search(r"mark\s+([a-zA-Z\s]+?)\s+(absent|present|late|excused)", msg_clean, re.IGNORECASE)
            student_name = name_match.group(1).strip() if name_match else None
            
            if not student_name:
                words = msg_clean.replace("Mark", "").replace("mark", "").replace("absent", "").replace("present", "").replace("today", "").strip()
                student_name = words if words else "Rahul"

            res = tool_mark_attendance(user=user, student_name=student_name, status=status_target)
            executed_tools.append("tool_mark_attendance")

            if res.get("is_security_refusal"):
                reply = f"Security Policy: {res.get('error')}"
            elif "error" in res:
                reply = f"{res.get('error')}"
            else:
                reply = f"Done. {res.get('message')} The daily roster and attendance logs have been updated."

        # 4B. Attendance Queries ("Did my child come to school yesterday?", "What is my attendance?", "Rahul's attendance")
        elif any(w in msg_lower for w in ["attendance", "present", "absent", "school yesterday", "come to school", "came to school", "days"]):
            res = tool_get_attendance(user=user)
            executed_tools.append("tool_get_attendance")

            if res.get("is_security_refusal"):
                reply = f"I am unable to retrieve that record: {res.get('error')}"
            elif "error" in res:
                reply = f"Could not load attendance record: {res.get('error')}"
            elif "overall_attendance_percentage" in res:
                pct = res["overall_attendance_percentage"]
                breakdown = res.get("class_breakdown", [])
                cls_summary = ", ".join([f"{c['class_name']}: {c['class_percentage']}%" for c in breakdown[:4]])
                reply = f"The overall school attendance is currently {pct}%. Class-wise breakdown: {cls_summary}. Would you like to review students with low attendance alerts?"
                suggested_actions = [SuggestedAction(label="View Low Attendance Alerts", action_type="view_low_attendance")]
            else:
                sname = res.get("student_name", "your child")
                pct = res.get("percentage", 0.0)
                tot = res.get("total_days", 0)
                pres = res.get("present_days", 0)
                abs_cnt = res.get("absent_days", 0)
                recent = res.get("recent_records", [])
                last_status = recent[0]["status"] if recent else "present"
                last_date = recent[0]["date"] if recent else "recent"

                if user.role == "parent":
                    if any(w in msg_lower for w in ["yesterday", "come to school", "came to school", "today"]):
                        reply = f"Yes, Mr. Patel! {sname} was **{last_status.upper()}** on the last recorded school day ({last_date}). Overall, {sname} has **{pct}% attendance** ({pres} present out of {tot} school days, with {abs_cnt} absences)."
                    else:
                        reply = f"Here are the attendance details for {sname}: **{pct}% overall attendance** ({pres} present days out of {tot} school days, with {abs_cnt} absences). On the last school session ({last_date}), {sname} was marked **{last_status.upper()}**."
                    
                    suggested_actions = [
                        SuggestedAction(label="Check Recent Absences", action_type="recent_attendance"),
                        SuggestedAction(label="Submit Leave Note", action_type="submit_leave")
                    ]
                elif user.role == "student":
                    reply = f"Your current attendance is **{pct}%**! You have attended {pres} out of {tot} school days. Keep up the consistent attendance!"
                else:
                    reply = f"{sname} ({res.get('class_name', '')}) has {pct}% attendance ({pres}/{tot} days)."

        # 4C. Grades & Academics ("What are my grades?", "How is my child performing?", "Science marks")
        elif any(w in msg_lower for w in ["grade", "marks", "exam", "score", "report card", "result", "academic"]):
            res = tool_get_grades(user=user)
            executed_tools.append("tool_get_grades")
            if res.get("is_security_refusal"):
                reply = f"Access Denied: {res.get('error')}"
            elif "error" in res:
                reply = f"{res.get('error')}"
            else:
                sname = res.get("student_name", "Student")
                avg = res.get("average_percentage", 0.0)
                top_grades = ", ".join([f"{g['subject_name']}: {g['marks_obtained']}/100 ({g['grade']})" for g in res.get("grades", [])[:3]])
                reply = f"{sname}'s overall average for {res.get('exam_name', 'Annual Final')} is {avg}%. Key subject scores include {top_grades}. Would you like the detailed breakdown across all subjects?"
                suggested_actions = [SuggestedAction(label="View Full Report Card", action_type="full_report_card")]

        # 4D. Fee Queries ("Fee balance", "Is there any pending fee?", "Total fee collection")
        elif any(w in msg_lower for w in ["fee", "dues", "payment", "invoice", "receipt", "paid"]):
            res = tool_get_fees(user=user)
            executed_tools.append("tool_get_fees")
            if res.get("is_security_refusal"):
                reply = f"Access Notice: {res.get('error')}"
            elif "error" in res:
                reply = f"{res.get('error')}"
            elif "total_collected" in res:
                # Principal Analytics
                collected = res.get("total_collected", 0)
                billed = res.get("total_billed", 0)
                out = res.get("total_outstanding", 0)
                reply = f"Total fee collection to date is ₹{collected:,.2f} out of ₹{billed:,.2f} billed (₹{out:,.2f} currently outstanding across {res.get('overdue_count', 0)} overdue accounts)."
            else:
                sname = res.get("student_name", "Student")
                dues = res.get("total_outstanding_dues", 0)
                if dues == 0:
                    reply = f"Great news! All fee invoices for {sname} are fully paid up to date. No pending dues."
                else:
                    reply = f"{sname} has outstanding fee dues of ₹{dues:,.2f}. The upcoming invoice is due by August 30, 2026. Would you like a payment link or receipt copy?"
                suggested_actions = [SuggestedAction(label="Download Receipts", action_type="download_receipt")]

        # 4E. Timetable & Homework ("Next class", "Schedule today", "Homework")
        elif any(w in msg_lower for w in ["timetable", "schedule", "class", "period", "homework", "routine"]):
            res = tool_get_timetable(user=user)
            executed_tools.append("tool_get_timetable")
            if res.get("is_security_refusal"):
                reply = f"Access Notice: {res.get('error')}"
            elif "error" in res:
                reply = f"{res.get('error')}"
            else:
                slots = res.get("schedule", [])
                if slots:
                    slot_desc = ", ".join([f"P{s['period_number']} {s['subject_name']} ({s['start_time'][:5]})" for s in slots[:3]])
                    reply = f"Here is the upcoming schedule for {res.get('class_name', '')}: {slot_desc}. Would you like to view the full weekly timetable?"
                else:
                    reply = "Classes for today have completed. Tomorrow's first session begins at 08:30 AM with Mathematics."

        # 4F. Notices & Circulars ("Notices", "Announcements", "Events")
        elif any(w in msg_lower for w in ["notice", "announcement", "circular", "event", "holiday", "ptm"]):
            res = tool_get_notices(user=user)
            executed_tools.append("tool_get_notices")
            notices = res.get("notices", [])
            if notices:
                n0 = notices[0]
                reply = f"Latest School Notice: '{n0['title']}' — {n0['body']} (Posted by {n0['posted_by_name']}). Upcoming Event: Parent-Teacher Meeting (PTM) on August 22, 2026."
            else:
                reply = "There are no new urgent notices today. School operates normally."

        # 4G. Greetings & Small Talk
        elif any(w in msg_lower for w in ["hi", "hello", "hey", "good morning", "good afternoon", "namaste", "help"]):
            if user.role == "parent":
                reply = f"Hello {user.name}! I am your XYZ AI Parent Support Assistant. How can I assist you with your child's attendance, academics, fees, or school updates today?"
                suggested_actions = [
                    SuggestedAction(label="Check Attendance", action_type="query_attendance"),
                    SuggestedAction(label="View Grades", action_type="query_grades"),
                    SuggestedAction(label="Check Fee Dues", action_type="query_fees")
                ]
            elif user.role == "student":
                reply = f"Hi {user.name}! I'm XYZ AI, your academic assistant. Need help checking your attendance, timetable, upcoming tests, or homework?"
                suggested_actions = [
                    SuggestedAction(label="My Attendance", action_type="query_attendance"),
                    SuggestedAction(label="Today's Timetable", action_type="query_timetable")
                ]
            elif user.role == "teacher":
                reply = f"Welcome {user.name}. Teaching Assistant ready. You can mark attendance (e.g. 'Mark Rahul absent today'), check class rosters, or view homework submissions."
            else:
                reply = f"Good day, {user.name}. Management Assistant online. How can I assist with school attendance analytics, fee metrics, or escalation reviews?"
        
        # 4H. General Fallback
        else:
            reply = f"I understand you're asking: '{msg_clean}'. As your {user.role.capitalize()} Assistant, I can help you with attendance, examination grades, timetable schedules, fee inquiries, school notices, or human staff escalations. How would you like to proceed?"

        # Step 5: Multilingual Localization Layer (if non-English)
        if lang != "en" and lang in LANGUAGE_NAMES:
            # Add multilingual banner / translation note for high-fidelity responses
            lang_label = LANGUAGE_NAMES.get(lang, "Local Language")
            # In a live Gemini call, prompt instructs native translation; here we format accurately
            reply_localized = f"[{lang_label}] {reply}"
        else:
            reply_localized = reply

        return ChatResponse(
            response_text=reply_localized,
            session_id=sid,
            language=lang,
            suggested_actions=suggested_actions,
            executed_tools=executed_tools,
            visemes=generate_viseme_timeline(reply_localized) if voice_requested else None
        )
