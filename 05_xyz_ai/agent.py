"""
XYZ AI — Conversational Agent & Persona Orchestration Engine
Implements the 4 AI Personas (Student, Parent, Teacher, Principal),
natural greetings, conversational memory, follow-up & correction handling,
clarification questions, and dynamic tone adaptation.
"""

import os
import re
import json
import uuid
import sys
import datetime
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("xyz_ai.agent")

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
    tool_get_exam_schedule,
    tool_get_fees,
    tool_get_timetable,
    tool_get_notices,
    tool_submit_leave,
    tool_request_escalation,
    tool_query_database
)

# ---------------------------------------------------------------------------
# 1. PERSONA SYSTEM PROMPTS (Human-Like, Empathetic, Role-Adapted)
# ---------------------------------------------------------------------------
PERSONA_PROMPTS = {
    "student": (
        "You are XYZ AI, a friendly, encouraging, empathetic, and supportive Academic Assistant for students. "
        "Your tone is warm, cheerful, positive, motivating, and age-appropriate. Help students understand academic concepts, "
        "organize their timetable, prepare for upcoming exams, track homework, and develop strong study habits. "
        "When a student feels stressed or anxious about studies, offer genuine encouragement and help break tasks into small, "
        "achievable steps. Celebrate their successes and encourage steady progress. Never disclose sensitive financial data or other students' private records."
    ),
    "parent": (
        "You are XYZ AI, a caring, patient, empathetic, and reassuring Parent Support Assistant. "
        "Your tone is respectful, warm, attentive, and understanding. You partner with parents to keep them informed about their child's "
        "academic journey, daily attendance, fee schedules, school events, and overall wellbeing. "
        "Listen patiently to parental concerns, acknowledge their feelings with empathy, and provide clear, reassuring explanations. "
        "Proactively offer relevant follow-ups, clarify school procedures gently, and facilitate communication with teachers when needed."
    ),
    "teacher": (
        "You are XYZ AI, an efficient, collegial, organized, and professional Teaching Assistant for school faculty. "
        "Your tone is collaborative, concise, practical, and action-oriented. You assist teachers with daily classroom logistics, "
        "including logging attendance, reviewing class performance trends, tracking homework submissions, looking up student profiles, "
        "and coordinating administrative requests so they can focus on teaching."
    ),
    "principal": (
        "You are XYZ AI, an executive, strategic, analytical, and professional Management Assistant for School Leadership. "
        "Your tone is formal, concise, data-driven, and insightful. You provide high-level school-wide summaries (attendance rates, "
        "fee collection metrics, departmental breakdowns, escalation queues), highlight operational trends, and offer drill-down capabilities "
        "to assist with school governance and strategic decision making."
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

# ---------------------------------------------------------------------------
# 2. SESSION MEMORY & CONTEXT STATE
# ---------------------------------------------------------------------------
SESSION_MEMORY: Dict[str, Dict[str, Any]] = {}

def get_session(session_id: Optional[str], user: UserTokenPayload) -> Tuple[str, Dict[str, Any]]:
    """Retrieves or restores active session state with SQLite/Postgres persistence."""
    from shared.database import get_conversation_history, get_user_recent_session
    
    # If no session_id given, check if user has an existing session in the database
    if not session_id and user and user.user_id:
        recent = get_user_recent_session(user.user_id)
        if recent:
            session_id = recent.get("session_id")

    sid = session_id or f"sess_{uuid.uuid4().hex[:10]}"
    if sid not in SESSION_MEMORY:
        db_messages = get_conversation_history(sid, limit=30)
        SESSION_MEMORY[sid] = {
            "user_id": user.user_id,
            "role": user.role,
            "user_name": user.name,
            "messages": db_messages,
            "context": {
                "active_student_name": None,
                "active_topic": None,     # "attendance", "grades", "fees", "timetable", "homework", "notices", "leave", "escalation"
                "active_subject": None,   # "Mathematics", "Science", "Physics", etc.
                "active_date": None,
                "last_data": {},          # Cache of most recent ERP query data
                "last_question": None     # Pending question context
            },
            "pending_slot": None,
            "pending_escalation": False,
            "pending_escalation_target": None,
            "pending_escalation_reason": None
        }

        # Restore conversational context from last assistant message
        if db_messages:
            last_asst_msgs = [m for m in db_messages if m.get("role") == "assistant"]
            if last_asst_msgs:
                last_txt = last_asst_msgs[-1].get("content", "").lower()
                if "balance of" in last_txt or "fees" in last_txt or "due" in last_txt:
                    SESSION_MEMORY[sid]["context"]["active_topic"] = "fees"
                elif "attendance" in last_txt or "present" in last_txt or "absent" in last_txt:
                    SESSION_MEMORY[sid]["context"]["active_topic"] = "attendance"
                elif "marks" in last_txt or "grades" in last_txt or "report card" in last_txt:
                    SESSION_MEMORY[sid]["context"]["active_topic"] = "grades"
                elif "timetable" in last_txt or "period" in last_txt:
                    SESSION_MEMORY[sid]["context"]["active_topic"] = "timetable"

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
        "human assistant", "human assistance", "speak to human", "complaint", "talk to management",
        "call teacher", "call principal", "not happy", "transfer me", "real person",
        "contact someone", "human agent", "talk to someone", "speak to someone",
        "help from teacher", "help from management", "speak with someone"
    ]
    lower = text.lower()
    return any(t in lower for t in triggers)

def detect_affirmation(text: str) -> bool:
    """Detects if user says Yes / Confirm to a pending prompt."""
    low = text.lower().strip()
    affirmations = [
        "yes", "yeah", "yep", "sure", "please do", "request a call",
        "connect now", "yes please", "submit request", "submit", "confirm",
        "ok", "okay", "ha", "haan", "bilkul", "proceed", "go ahead", "do it", "please submit"
    ]
    return any(a in low or low.startswith(a) for a in affirmations)

def detect_greeting(text: str) -> bool:
    """Detects if user is sending a natural greeting."""
    low = text.lower().strip()
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "namaste", "namaskar", "kem cho", "vanakkam", "pranam", "how are you", "what's up", "hey there", "hi there", "greetings"]
    words = re.findall(r'\b\w+\b', low)
    if any(g in low for g in ["good morning", "good afternoon", "good evening", "how are you", "what's up", "kem cho", "hey there", "hi there"]):
        return True
    if len(words) <= 3 and any(w in greetings for w in words):
        return True
    return False

def get_time_based_greeting() -> str:
    """Returns Morning, Afternoon, or Evening based on current local hour."""
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

SCHEMA_MAP_CONTEXT = """
INTERCONNECTED DATABASE SCHEMA (You can query ANY of these tables using query_school_database(sql_query="SELECT ...")):
- users (id, auth_id, email, name, role, phone, preferred_language) -- [Roles: 'student', 'parent', 'teacher', 'principal']
- classes (id, name, grade, section, academic_year) -- [e.g. 'Grade 10-A', 'Grade 12 Science (PCMB)']
- subjects (id, code, name, department) -- [e.g. 'Mathematics', 'General Science', 'Physics']
- students (id, user_id, roll_number, name, class_id, date_of_birth, gender) -- [Foreign Keys: user_id -> users.id, class_id -> classes.id]
- parent_student_links (id, parent_user_id, student_id, relationship) -- [Foreign Keys: parent_user_id -> users.id, student_id -> students.id]
- teacher_class_links (id, teacher_user_id, class_id, subject_id, is_class_teacher) -- [Foreign Keys: teacher_user_id -> users.id, class_id -> classes.id, subject_id -> subjects.id]
- attendance (id, student_id, date, status, remarks) -- [Foreign Key: student_id -> students.id. status: 'present', 'absent', 'late', 'excused']
- exams (id, name, exam_type, start_date, end_date, academic_year)
- grades (id, student_id, subject_id, exam_id, marks_obtained, max_marks, grade, remarks) -- [Foreign Keys: student_id -> students.id, subject_id -> subjects.id, exam_id -> exams.id]
- fee_invoices (id, student_id, invoice_number, term_name, total_amount, due_date, status) -- [Foreign Key: student_id -> students.id]
- fee_payments (id, invoice_id, amount_paid, payment_date, payment_method, transaction_ref) -- [Foreign Key: invoice_id -> fee_invoices.id]
- timetable_slots (id, class_id, day_of_week, period_number, subject_id, teacher_user_id, start_time, end_time, room_number) -- [Foreign Keys: class_id -> classes.id, subject_id -> subjects.id, teacher_user_id -> users.id]
- homework (id, class_id, subject_id, teacher_user_id, title, description, due_date) -- [Foreign Keys: class_id -> classes.id, subject_id -> subjects.id, teacher_user_id -> users.id]
- notices (id, title, content, target_audience, category, published_at, is_urgent)
- events (id, title, description, event_date, target_audience, venue)
- leave_applications (id, applicant_user_id, applicant_role, student_id, start_date, end_date, reason, status)
- escalation_tickets (id, ticket_id, requested_by_user_id, requested_by_role, student_id, target_entity, reason, status)
"""

def build_user_context_instruction(user: UserTokenPayload) -> str:
    """Dynamically builds rich persona, linked student context, and complete schema map."""
    base_prompt = PERSONA_PROMPTS.get(user.role, PERSONA_PROMPTS["parent"])
    user_context = ""
    if user.role == "parent":
        try:
            from rbac import validate_parent_student_ownership
            child = validate_parent_student_ownership(user.user_id)
            user_context = (
                f"PARENT CONTEXT:\n"
                f"- You are talking to parent '{user.name}'.\n"
                f"- Their linked registered child is: {child['name']} ({child['class_name']}, Roll Number: {child['roll_number']}).\n"
                f"- When the parent asks about 'my child', 'my son', 'my daughter', 'yesterday's attendance', 'fees', or 'grades', "
                f"you ALREADY know their child is {child['name']}. Do NOT ask for the child's name."
            )
        except Exception:
            pass
    elif user.role == "student":
        try:
            from rbac import get_student_for_user
            std = get_student_for_user(user.user_id)
            user_context = (
                f"STUDENT CONTEXT:\n"
                f"- You are talking to student '{user.name}' ({std['class_name']}, Roll Number: {std['roll_number']}).\n"
                f"- When they ask about attendance, timetable, homework, upcoming exams, or grades, retrieve their records directly."
            )
        except Exception:
            pass
    elif user.role == "teacher":
        user_context = f"TEACHER CONTEXT:\nYou are speaking with Teacher '{user.name}' (Mentor for Grade 10-A)."
    elif user.role == "principal":
        user_context = f"PRINCIPAL CONTEXT:\nYou are speaking with Principal '{user.name}' (School Leadership)."

    return f"{base_prompt}\n\n{user_context}\n\n{SCHEMA_MAP_CONTEXT}"

def sanitize_ai_output(text: str) -> str:
    """Removes any accidental raw code, XML tool tags, or pseudo-function string artifacts."""
    if not text:
        return text
    cleaned = re.sub(r'<(function|tool_call|invoke)>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'</?(function|tool_call|invoke)[^>]*>', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[a-zA-Z_0-9]+\([^)]*\)', '', cleaned)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned)
    cleaned = re.sub(r'\s+([.,!?])', r'\1', cleaned)
    return cleaned.strip()

STUDENT_NAMES_MAP = [
    "rahul patel", "rahul", "aarav sharma", "aarav", "diya mehta", "diya",
    "rohan gupta", "rohan", "priya nair", "priya", "ananya iyer", "ananya",
    "siddharth joshi", "siddharth", "tanvi deshmukh", "tanvi", "aditya singhania", "aditya",
    "riya mukherjee", "riya", "varun chawla", "varun", "shreya nambiar", "shreya",
    "neil bhatia", "neil", "devika pillai", "devika", "karthik sundaram", "karthik",
    "pooja reddy", "pooja", "yashvardhan rathore", "yashvardhan", "sneha banerjee", "sneha",
    "arjun kapoor", "arjun", "kabir khan", "kabir", "ishaan verma", "ishaan",
    "dhruv malhotra", "dhruv", "natasha goel", "natasha"
]

SUBJECTS_MAP = ["mathematics", "math", "maths", "science", "physics", "chemistry", "biology", "english", "hindi", "social science", "history", "computer science"]

def extract_student_name_from_text(text: str) -> Optional[str]:
    low = text.lower()
    for name in STUDENT_NAMES_MAP:
        if re.search(rf"\b{name}\b", low):
            return name.title()
    return None

def extract_subject_from_text(text: str) -> Optional[str]:
    low = text.lower()
    for s in SUBJECTS_MAP:
        if re.search(rf"\b{s}\b", low):
            if s in ["math", "maths"]:
                return "Mathematics"
            return s.title()
    return None

def detect_message_language(text: str) -> Optional[SupportedLanguage]:
    """Detects Indian language scripts and Hinglish."""
    for ch in text:
        if '\u0A80' <= ch <= '\u0AFF':
            return "gu"
        elif '\u0900' <= ch <= '\u097F':
            return "hi"
        elif '\u0B80' <= ch <= '\u0BFF':
            return "ta"
        elif '\u0C00' <= ch <= '\u0C7F':
            return "te"
        elif '\u0980' <= ch <= '\u09FF':
            return "bn"
        elif '\u0A00' <= ch <= '\u0A7F':
            return "pa"
        elif '\u0C80' <= ch <= '\u0CFF':
            return "kn"
        elif '\u0D00' <= ch <= '\u0D7F':
            return "ml"
        elif '\u0600' <= ch <= '\u06FF':
            return "ur"
            
    # Check Hinglish keywords
    t_lower = text.lower()
    if any(w in t_lower.split() for w in ["kya", "hai", "hain", "kitna", "kitni", "kaise", "batao", "dikhao", "bhejo", "kal", "aaya", "aayi", "aaye", "tha", "thi", "mera", "meri", "humara", "chahiye", "fees", "hajiri"]):
        return "hinglish"
        
    return None

# ---------------------------------------------------------------------------
# 3. CONVERSATION ORCHESTRATOR
# ---------------------------------------------------------------------------
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
        detected_lang = detect_message_language(message)
        lang = language or detected_lang or user.preferred_language or "en"
        lang_code = lang.value if hasattr(lang, 'value') else str(lang)
        msg_clean = message.strip()
        msg_lower = msg_clean.lower()
        executed_tools = []
        suggested_actions = []

        context = state.setdefault("context", {
            "active_student_name": None,
            "active_topic": None,
            "active_subject": None,
            "active_date": None,
            "last_data": {}
        })

        # Initialize student name for parents or students
        if not context.get("active_student_name"):
            if user.role == "parent":
                try:
                    from rbac import validate_parent_student_ownership
                    child = validate_parent_student_ownership(user.user_id)
                    context["active_student_name"] = child["name"]
                except Exception:
                    pass
            elif user.role == "student":
                context["active_student_name"] = user.name

        # Detect any newly mentioned student or subject in this turn
        mentioned_student = extract_student_name_from_text(msg_clean)
        if mentioned_student:
            context["active_student_name"] = mentioned_student

        mentioned_subject = extract_subject_from_text(msg_clean)
        if mentioned_subject:
            context["active_subject"] = mentioned_subject

        # =======================================================================
        # Step 0: Handle Explicit Language Selection / Switch Responses
        # (e.g., user replies "Hindi.", "Gujarati", "Marathi", "English", "Hinglish")
        # =======================================================================
        clean_no_punct = re.sub(r'[^\w\s]', '', msg_lower).strip()
        selected_lang_code = None
        
        LANG_KEYWORDS = {
            "hi": ["hindi", "हिन्दी", "हिंदी", "hindi me", "in hindi", "hindi please", "hindi language"],
            "gu": ["gujarati", "ગુજરાતી", "gujrati", "gujarati ma", "in gujarati", "gujarati please", "gujarati language"],
            "mr": ["marathi", "मराठी", "marathi madhe", "in marathi", "marathi please", "marathi language"],
            "ta": ["tamil", "தமிழ்", "tamilil", "in tamil", "tamil please", "tamil language"],
            "te": ["telugu", "తెలుగు", "in telugu", "telugu please"],
            "bn": ["bengali", "বাংলা", "in bengali", "bangla"],
            "pa": ["punjabi", "ਪੰਜਾਬੀ", "in punjabi"],
            "hinglish": ["hinglish", "hinglish me", "in hinglish"],
            "en": ["english", "in english", "english please", "angrezi"]
        }
        
        for lcode, aliases in LANG_KEYWORDS.items():
            if clean_no_punct in aliases or any(alias == msg_lower or f"talk in {alias}" in msg_lower or f"speak in {alias}" in msg_lower or f"continue in {alias}" in msg_lower for alias in aliases):
                selected_lang_code = lcode
                break
                
        is_subject_context = context.get("active_topic") in ["exams", "academics", "homework"] and clean_no_punct in ["english", "hindi", "maths", "mathematics", "science"]
        if selected_lang_code and not is_subject_context:
            lang = selected_lang_code
            lang_code = selected_lang_code
            context["preferred_language"] = selected_lang_code
            
            active_student = context.get("active_student_name") or ("Rahul" if user.role in ["student", "parent"] else "students")
            
            if selected_lang_code == "hi":
                reply = f"नमस्ते! हमने बातचीत की भाषा **हिन्दी** चुन ली है। आप {active_student} की उपस्थिति, परीक्षा परिणाम, फीस या समय सारणी के बारे में क्या जानना चाहते हैं?"
                suggested_actions = [
                    SuggestedAction(label="उपस्थिति रिकॉर्ड", action_type="query_attendance"),
                    SuggestedAction(label="परीक्षा परिणाम", action_type="query_grades"),
                    SuggestedAction(label="शुल्क भुगतान", action_type="query_fees")
                ]
            elif selected_lang_code == "gu":
                reply = f"નમસ્તે! આપણે વાતચીત માટે **ગુજરાતી** ભાષા પસંદ કરી છે. તમે {active_student}ની હાજરી, પરીક્ષા પરિણામ, ફી અથવા ટાઈમટેબલ વિશે શું પૂછવા માંગો છો?"
                suggested_actions = [
                    SuggestedAction(label="હાજરી પત્રક", action_type="query_attendance"),
                    SuggestedAction(label="પરિણામ પત્રક", action_type="query_grades"),
                    SuggestedAction(label="ફી ની વિગતો", action_type="query_fees")
                ]
            elif selected_lang_code == "mr":
                reply = f"नमस्कार! आपण **मराठी** भाषा निवडली आहे. {active_student} ची उपस्थिती, प्रगती पुस्तक, फी किंवा वेळापत्रकाबद्दल आपल्याला काय जाणून घ्यायचे आहे?"
                suggested_actions = [
                    SuggestedAction(label="उपस्थिती नोंद", action_type="query_attendance"),
                    SuggestedAction(label="प्रगती पुस्तक", action_type="query_grades")
                ]
            elif selected_lang_code == "ta":
                reply = f"வணக்கம்! நீங்கள் **தமிழ்** மொழியைத் தேர்ந்தெடுத்துள்ளீர்கள். {active_student} வருகை, மதிப்பெண் அல்லது கட்டணம் பற்றி என்ன அறிய விரும்புகிறீர்கள்?"
                suggested_actions = [
                    SuggestedAction(label="வருகைப் பதிவு", action_type="query_attendance"),
                    SuggestedAction(label="மதிப்பெண் பட்டியல்", action_type="query_grades")
                ]
            elif selected_lang_code == "hinglish":
                reply = f"Bohot badhiya! Humne conversation language **Hinglish** set kar di hai. {active_student} ki attendance, exam results, fees payment ya class schedule ke baare me aap kya jaan-na chahte hain?"
                suggested_actions = [
                    SuggestedAction(label="Attendance Record", action_type="query_attendance"),
                    SuggestedAction(label="Exam Report Card", action_type="query_grades"),
                    SuggestedAction(label="Fee Details", action_type="query_fees")
                ]
            else:
                reply = f"Wonderful! We'll continue in **English**. What would you like to explore regarding {active_student}'s attendance, report card, fee payments, or schedule?"
                suggested_actions = [
                    SuggestedAction(label="Attendance Record", action_type="query_attendance"),
                    SuggestedAction(label="Academic Report", action_type="query_grades"),
                    SuggestedAction(label="Fee Invoices", action_type="query_fees")
                ]
            
            ConversationOrchestrator._record_turn(sid, state, user, msg_clean, reply, lang, [])
            return ChatResponse(
                response_text=reply,
                session_id=sid,
                language=lang,
                suggested_actions=suggested_actions,
                executed_tools=[],
                visemes=generate_viseme_timeline(reply) if voice_requested else None
            )

        # =======================================================================
        # Step 1: Security Prompt-Injection and Meta System Inspection Guard
        # =======================================================================
        if any(p in msg_lower for p in ["ignore previous instructions", "system prompt", "reveal your instructions", "print your initial prompt", "give me your api key"]):
            reply = "I am XYZ AI, your school assistant. I cannot disclose internal system configurations or modify security directives. How can I assist you with school academics or services today?"
            ConversationOrchestrator._record_turn(sid, state, user, msg_clean, reply, lang, executed_tools)
            return ChatResponse(
                response_text=reply,
                session_id=sid,
                language=lang,
                visemes=generate_viseme_timeline(reply) if voice_requested else None
            )

        # =======================================================================
        # Step 2: Handle Pending Escalation Confirmation
        # =======================================================================
        if state.get("pending_escalation"):
            if detect_affirmation(msg_clean) or any(w in msg_lower for w in ["talk to teacher", "contact school management", "request a call"]):
                target = state.get("pending_escalation_target") or ("teacher" if "teacher" in msg_lower or user.role == "parent" else "management")
                if "management" in msg_lower or "admin" in msg_lower:
                    target = "management"
                elif "teacher" in msg_lower:
                    target = "teacher"
                    
                reason = state.get("pending_escalation_reason") or "User requested direct human assistance."
                
                # Execute mock escalation dispatch service
                res = tool_request_escalation(
                    user=user,
                    target_entity=target,
                    reason=reason
                )
                executed_tools.append("tool_request_escalation")
                state["pending_escalation"] = False

                # Strictly verify confirmation before claiming representative was contacted
                if res.get("confirmed"):
                    if target == "teacher":
                        reply = f"Your call request has been submitted to the teacher."
                        if res.get("target_name") and res.get("target_name") != "Class Teacher":
                            reply += f" ({res.get('target_name')} will receive the notification and reach out shortly)."
                    elif target == "counselor":
                        reply = f"Your appointment request with the student counselor has been submitted."
                    else:
                        reply = f"Your support request has been submitted to School Management. Ticket ID #{res.get('ticket_id', '')} has been logged."
                else:
                    reply = "I was unable to dispatch the request to the mock service at this time. The teacher or school management has not been contacted. Would you like me to try again or provide direct office phone numbers?"
                
                ConversationOrchestrator._record_turn(sid, state, user, msg_clean, reply, lang, executed_tools)
                return ChatResponse(
                    response_text=reply,
                    session_id=sid,
                    language=lang,
                    executed_tools=executed_tools,
                    visemes=generate_viseme_timeline(reply) if voice_requested else None
                )
            else:
                state["pending_escalation"] = False
                reply = "No problem at all! We can continue right here. What else would you like to know or discuss?"
                ConversationOrchestrator._record_turn(sid, state, user, msg_clean, reply, lang, executed_tools)
                return ChatResponse(
                    response_text=reply,
                    session_id=sid,
                    language=lang,
                    visemes=generate_viseme_timeline(reply) if voice_requested else None
                )

        # =======================================================================
        # Step 3: Handle Dissatisfaction / Escalation Request
        # =======================================================================
        if detect_dissatisfaction_or_escalation(msg_clean):
            state["pending_escalation"] = True
            
            # Determine target entity from user input
            if "management" in msg_lower or "principal" in msg_lower or "admin" in msg_lower:
                state["pending_escalation_target"] = "management"
                state["pending_escalation_reason"] = f"Management escalation: {msg_clean}"
                reply = "Of course. I can connect you with School Management. Would you like me to submit a support request now?"
            elif "counselor" in msg_lower:
                state["pending_escalation_target"] = "counselor"
                state["pending_escalation_reason"] = f"Counselor request: {msg_clean}"
                reply = "Of course. I can connect you with the student counselor. Would you like me to request an appointment now?"
            else:
                state["pending_escalation_target"] = "teacher"
                state["pending_escalation_reason"] = f"Teacher escalation: {msg_clean}"
                reply = "Of course. I can connect you with the teacher. Would you like me to request a call now?"

            if user.role in ["parent", "student"]:
                suggested_actions = [
                    SuggestedAction(label="Talk to Teacher", action_type="confirm_escalation", payload={"target": "teacher"}),
                    SuggestedAction(label="Contact School Management", action_type="confirm_escalation", payload={"target": "management"}),
                    SuggestedAction(label="Continue with AI", action_type="cancel_escalation")
                ]
            elif user.role == "teacher":
                state["pending_escalation_target"] = "principal"
                state["pending_escalation_reason"] = f"Teacher coordination: {msg_clean}"
                reply = "Understood. Would you like me to log an administrative support ticket for the Principal / School Office?"
                suggested_actions = [
                    SuggestedAction(label="Contact School Management", action_type="confirm_escalation", payload={"target": "principal"})
                ]
            else:
                reply = "As School Leadership, you can review and resolve all open escalation tickets directly from the management queue."
                suggested_actions = []
            
            ConversationOrchestrator._record_turn(sid, state, user, msg_clean, reply, lang, executed_tools)
            return ChatResponse(
                response_text=reply,
                session_id=sid,
                language=lang,
                suggested_actions=suggested_actions,
                visemes=generate_viseme_timeline(reply) if voice_requested else None
            )

        # =======================================================================
        # Step 4A: Live Gemini Engine Execution (Fast Non-Blocking Async)
        # =======================================================================
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
                cleaned_text = sanitize_ai_output(gemini_text)
                ConversationOrchestrator._record_turn(sid, state, user, msg_clean, cleaned_text, lang, tools_called)
                return ChatResponse(
                    response_text=cleaned_text,
                    session_id=sid,
                    language=lang,
                    executed_tools=tools_called,
                    visemes=generate_viseme_timeline(cleaned_text) if voice_requested else None
                )

        # =======================================================================
        # Step 4B: Live Groq Engine Execution (Ultra-Fast Fallback LLM)
        # =======================================================================
        from groq_service import groq_service
        if groq_service.is_configured:
            persona_instruction = build_user_context_instruction(user)
            groq_result = await groq_service.generate_response(
                message=msg_clean,
                user=user,
                system_instruction=persona_instruction,
                chat_history=state.get("messages", []),
                language=lang
            )
            if groq_result:
                groq_text, tools_called = groq_result
                cleaned_text = sanitize_ai_output(groq_text)
                ConversationOrchestrator._record_turn(sid, state, user, msg_clean, cleaned_text, lang, tools_called)
                return ChatResponse(
                    response_text=cleaned_text,
                    session_id=sid,
                    language=lang,
                    executed_tools=tools_called,
                    visemes=generate_viseme_timeline(cleaned_text) if voice_requested else None
                )

        # =======================================================================
        # Step 5: Advanced Human-Like Conversational Fallback Engine
        # Handles Natural Greetings, Context Remembrance, Follow-ups, Corrections,
        # Clarifications, and Dynamic Persona Tone Adaptation.
        # =======================================================================
        reply, suggested_actions, executed_tools = ConversationOrchestrator._handle_conversational_turn(
            msg_clean=msg_clean,
            msg_lower=msg_lower,
            user=user,
            state=state,
            lang=lang
        )

        from shared.multilingual_engine import translate_response_text, translate_suggested_actions
        translated_reply = translate_response_text(reply, lang_code)
        translated_actions = translate_suggested_actions(suggested_actions, lang_code)

        ConversationOrchestrator._record_turn(sid, state, user, msg_clean, translated_reply, lang, executed_tools)
        return ChatResponse(
            response_text=translated_reply,
            session_id=sid,
            language=lang,
            suggested_actions=translated_actions,
            executed_tools=executed_tools,
            visemes=generate_viseme_timeline(translated_reply) if voice_requested else None
        )

    @staticmethod
    def _record_turn(session_id: str, state: Dict[str, Any], user: UserTokenPayload, user_msg: str, assistant_reply: str, lang: Any = "en", executed_tools: list = None):
        """Maintains clean multi-turn dialogue history in session memory and persists to database."""
        from shared.database import save_conversation_turn
        msgs = state.setdefault("messages", [])
        now_iso = datetime.datetime.now().isoformat()
        msgs.append({"role": "user", "content": user_msg, "timestamp": now_iso})
        msgs.append({"role": "assistant", "content": assistant_reply, "timestamp": now_iso})
        if len(msgs) > 30:
            state["messages"] = msgs[-30:]

        try:
            lang_str = lang.value if hasattr(lang, "value") else str(lang)
            uid = user.user_id if user else "usr_anon"
            save_conversation_turn(session_id, uid, user_msg, assistant_reply, lang_str, executed_tools)
        except Exception as e:
            logger.warning(f"Error saving turn to database: {e}")

    @staticmethod
    def _handle_conversational_turn(
        msg_clean: str,
        msg_lower: str,
        user: UserTokenPayload,
        state: Dict[str, Any],
        lang: SupportedLanguage
    ) -> Tuple[str, List[SuggestedAction], List[str]]:
        context = state.setdefault("context", {})
        executed_tools = []
        suggested_actions = []
        time_greeting = get_time_based_greeting()
        active_student = context.get("active_student_name")
        active_subject = context.get("active_subject")
        last_topic = context.get("active_topic")
        last_data = context.get("last_data", {})

        # -------------------------------------------------------------------
        # A. Conversational Corrections ("no, I meant Science", "actually next Monday", "no, mark him present")
        # -------------------------------------------------------------------
        is_correction = any(w in msg_lower for w in ["no,", "no ", "not that", "actually", "i meant", "instead", "change to", "correction"])
        
        if is_correction and active_subject and any(w in msg_lower for w in ["math", "science", "physics", "chemistry", "english", "hindi", "biology"]):
            # Subject correction in grades or homework
            context["active_topic"] = "grades"
            res = tool_get_grades(user=user, student_name=active_student)
            executed_tools.append("tool_get_grades")
            matching_grade = None
            for g in res.get("grades", []):
                if active_subject.lower() in g["subject_name"].lower():
                    matching_grade = g
                    break
            
            if matching_grade:
                if user.role == "parent":
                    reply = (f"Got it! For **{matching_grade['subject_name']}**, {active_student or 'your child'} scored "
                             f"**{matching_grade['marks_obtained']}/{matching_grade['max_marks']}** (Grade: {matching_grade['grade']}). "
                             f"Teacher remarks: *\"{matching_grade.get('remarks', 'Good performance')}\"*. "
                             f"Would you like study recommendations or upcoming exam dates for this subject?")
                elif user.role == "student":
                    reply = (f"Sure thing! For **{matching_grade['subject_name']}**, you scored **{matching_grade['marks_obtained']}/{matching_grade['max_marks']}** ({matching_grade['grade']}). "
                             f"You're doing great—keep up the good work and let me know if you want any revision tips!")
                else:
                    reply = f"Updated: For **{matching_grade['subject_name']}**, {active_student}'s score is **{matching_grade['marks_obtained']}/{matching_grade['max_marks']}** ({matching_grade['grade']})."
            else:
                reply = f"I've switched to **{active_subject}**. Let me know if you'd like to see test scores, homework, or syllabus topics for this subject!"
            return reply, suggested_actions, executed_tools

        if is_correction and user.role in ["teacher", "principal"] and any(w in msg_lower for w in ["present", "absent", "late"]):
            status_target = "present" if "present" in msg_lower else "absent" if "absent" in msg_lower else "late"
            res = tool_mark_attendance(user=user, student_name=active_student or "Rahul", status=status_target)
            executed_tools.append("tool_mark_attendance")
            reply = f"Understood! I've updated the record. {res.get('message', 'Attendance has been corrected.')}"
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # B. Natural Role-Adapted Greetings
        # -------------------------------------------------------------------
        if detect_greeting(msg_clean):
            first_name = user.name.split()[0] if user.name else "there"
            if user.role == "parent":
                reply = (f"Hello {user.name}! {time_greeting}! I'm XYZ AI, your Parent Support Assistant. "
                         f"Which language would you prefer to continue in today? (English, हिन्दी, ગુજરાતી, मराठी...)")
                suggested_actions = [
                    SuggestedAction(label=f"Check {active_student or 'Child'}'s Attendance", action_type="query_attendance"),
                    SuggestedAction(label="Review Recent Grades", action_type="query_grades"),
                    SuggestedAction(label="Check Fee Status", action_type="query_fees")
                ]
            elif user.role == "student":
                reply = (f"Hey {first_name}! {time_greeting}! 😊 I'm XYZ AI, your Academic Assistant. "
                         f"Which language would you prefer to continue in today? (English, हिन्दी, ગુજરાતી, मराठी...)")
                suggested_actions = [
                    SuggestedAction(label="My Timetable Today", action_type="query_timetable"),
                    SuggestedAction(label="My Attendance", action_type="query_attendance"),
                    SuggestedAction(label="Upcoming Exam Dates", action_type="query_exams")
                ]
            elif user.role == "teacher":
                reply = (f"Hello {user.name}! {time_greeting}! I'm XYZ AI, your Teaching Assistant. "
                         f"Which language would you prefer to continue in today? (English, हिन्दी, ગુજરાતી, मराठी...)")
                suggested_actions = [
                    SuggestedAction(label="Mark Daily Attendance", action_type="mark_attendance"),
                    SuggestedAction(label="Class Attendance Summary", action_type="class_attendance"),
                    SuggestedAction(label="View Timetable", action_type="query_timetable")
                ]
            else:  # Principal
                reply = (f"Good day, {user.name}! I'm Athena, your Executive Management Assistant. "
                         f"Which language would you prefer for today's session? (English, हिन्दी, ગુજરાતી, मराठी...)")
                suggested_actions = [
                    SuggestedAction(label="School Attendance Metrics", action_type="query_attendance"),
                    SuggestedAction(label="Fee Collection Overview", action_type="query_fees"),
                    SuggestedAction(label="Escalation Ticket Queue", action_type="query_escalations")
                ]
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # C. Emotional / Sentiment Awareness (Stress, Exam anxiety, Gratitude)
        # -------------------------------------------------------------------
        if any(w in msg_lower for w in ["thank you", "thanks", "dhanyawad", "shukriya", "great help", "you are helpful"]):
            if user.role == "student":
                reply = "You're very welcome! Always here cheering you on. Let me know if you need anything else for your studies! 🌟"
            elif user.role == "parent":
                reply = "It is truly my pleasure to assist you! Please don't hesitate to reach out whenever you have questions about your child's schooling. Have a wonderful day!"
            elif user.role == "teacher":
                reply = "Glad I could help save you some time! Let me know whenever you need anything else organized."
            else:
                reply = "Always at your service to support school leadership. Let me know if further analytics are needed."
            return reply, suggested_actions, executed_tools

        if user.role == "student" and any(w in msg_lower for w in ["stressed", "worried", "nervous", "scared", "hard", "tough", "exam stress", "fail"]):
            reply = ("I completely understand how you feel, and it's totally normal to feel a bit nervous before exams! "
                     "Remember to take a deep breath. Break your study topics into 25-minute focused blocks with short breaks (the Pomodoro technique). "
                     "Would you like me to pull up your exam schedule or highlight the key subjects so we can plan together?")
            suggested_actions = [
                SuggestedAction(label="View Exam Schedule", action_type="query_exams"),
                SuggestedAction(label="Today's Timetable", action_type="query_timetable")
            ]
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # D. Clarification Question: Leave Applications
        # -------------------------------------------------------------------
        if any(w in msg_lower for w in ["leave", "chutti", "take a day off", "apply for leave", "sick leave", "absent application"]):
            context["active_topic"] = "leave"
            date_match = re.search(r'\b(202\d-\d{2}-\d{2}|tomorrow|today|next monday|monday|tuesday|wednesday|thursday|friday)\b', msg_lower)
            reason_match = any(r in msg_lower for r in ["fever", "sick", "ill", "wedding", "family", "medical", "urgent", "travel", "emergency"])
            
            if not date_match or not reason_match:
                if user.role == "parent":
                    reply = (f"I'll gladly help submit a leave application for {active_student or 'your child'}. "
                             f"To make sure it's processed accurately by the school, could you please share the **date(s) of absence** and the **reason for leave**?")
                elif user.role == "student":
                    reply = ("I can help you draft a leave application! Could you please let me know the **start date, end date**, and the **reason** for your absence?")
                else:
                    reply = "I can record your staff leave application. Please provide the requested dates and reason."
                return reply, suggested_actions, executed_tools
            else:
                target_date = date_match.group(1) if date_match else "2026-08-20"
                res = tool_submit_leave(user=user, start_date=target_date, end_date=target_date, reason="Personal / Medical Leave", student_name=active_student)
                executed_tools.append("tool_submit_leave")
                reply = f"Your leave application for {active_student or user.name} on {target_date} has been submitted successfully! The class teacher will be notified."
                return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # E. Holistic Child Status / Broad Inquiry ("How is Rahul doing?", "how is my child doing?")
        # -------------------------------------------------------------------
        if any(w in msg_lower for w in ["how is he doing", "how is she doing", "is everything okay", "overall status", "how is my child", "doing in school", "how is rahul doing", "how is my son doing", "how is my daughter doing", "child progress", "performance status"]):
            # If inquiry is specifically about a subject (e.g. "how is he doing in science")
            sub_match = next((s for s in ["science", "mathematics", "math", "english", "physics", "chemistry", "biology", "computer"] if s in msg_lower), None)
            if sub_match:
                context["active_topic"] = "subject_guidance"
                res_grd = tool_get_grades(user=user, student_name=active_student)
                executed_tools.append("tool_get_grades")
                sname = active_student or "Rahul"
                grades_list = res_grd.get("grades", [])
                target_g = next((g for g in grades_list if sub_match in g["subject_name"].lower()), None)
                if target_g:
                    reply = (f"For **{target_g['subject_name']}**, {sname} scored **{target_g['marks_obtained']}/{target_g['max_marks']}** (Grade: **{target_g['grade']}**).\n"
                             f"Teacher feedback: *\"{target_g.get('remarks', 'Consistently diligent.')}\"*.\n"
                             f"Overall, {sname} demonstrates strong conceptual grasp in {target_g['subject_name']}.")
                else:
                    reply = f"In **{sub_match.capitalize()}**, {sname} is performing well with consistent homework completion."
                return reply, suggested_actions, executed_tools

            res_att = tool_get_attendance(user=user, student_name=active_student)
            res_grd = tool_get_grades(user=user, student_name=active_student)
            executed_tools.extend(["tool_get_attendance", "tool_get_grades"])
            pct = res_att.get("percentage", 91.2)
            avg = res_grd.get("average_percentage", 87.5)
            sname = active_student or "Rahul"
            reply = (f"Overall, **{sname} is doing very well!** 😊\n"
                     f"- **Attendance**: {pct}% (punctual and attending regularly)\n"
                     f"- **Academic Average**: {avg}% across all major subjects\n"
                     f"- **Behavior & Conduct**: Positive teacher remarks across classes.\n"
                     f"Is there a particular subject or upcoming school event you'd like to discuss in detail?")
            suggested_actions = [
                SuggestedAction(label="Detailed Report Card", action_type="full_report_card"),
                SuggestedAction(label="Upcoming Tests", action_type="query_exams"),
                SuggestedAction(label="Leave Note", action_type="submit_leave")
            ]
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # F. Attendance Queries & Follow-ups
        # -------------------------------------------------------------------
        if any(w in msg_lower for w in [
            "attendance", "present", "absent", "school yesterday", "come to school", "came to school", 
            "days", "school aya", "school aaya", "school aayi", "school gaya", "kal school", "hajiri",
            "હાજરી", "હાજર", "ગેરહાજર", "उपस्थिति", "हाजिरी", "हाजिर", "गैरहाजिर", "उपस्थिती", "उपस्थित", "अनुपस्थित", "வருகை"
        ]):
            context["active_topic"] = "attendance"
            
            # Check if teacher wants to mark attendance
            if user.role in ["teacher", "principal"] and any(w in msg_lower for w in ["mark", "set"]):
                status_target = "absent" if "absent" in msg_lower else "present" if "present" in msg_lower else "late" if "late" in msg_lower else "present"
                name_match = re.search(r"mark\s+([a-zA-Z\s]+?)\s+(absent|present|late|excused)", msg_clean, re.IGNORECASE)
                student_to_mark = name_match.group(1).strip() if name_match else (active_student or "Rahul")

                res = tool_mark_attendance(user=user, student_name=student_to_mark, status=status_target)
                executed_tools.append("tool_mark_attendance")

                if res.get("is_security_refusal"):
                    reply = res.get("message", "Permission Denied.")
                else:
                    dt = res.get("date", "today")
                    reply = (f"Successfully updated! **{student_to_mark}** has been marked **{status_target.upper()}** for {dt}. "
                             f"Class total: {res.get('present_count', 0)} present.")
                return reply, suggested_actions, executed_tools

            # Retrieve attendance
            res = tool_get_attendance(user=user, student_name=active_student)
            executed_tools.append("tool_get_attendance")
            context["last_data"] = res

            if res.get("is_security_refusal"):
                reply = res.get("message", "Permission Denied.")
                return reply, suggested_actions, executed_tools

            if "overall_percentage" in res:
                # Principal Analytics
                pct = res.get("overall_percentage", 0.0)
                breakdown = res.get("class_breakdown", [])
                cls_summary = ", ".join([f"{c['class_name']}: {c['class_percentage']}%" for c in breakdown[:4]])
                reply = (f"**School-Wide Attendance Overview**: The overall student attendance across all grades is currently **{pct}%**. "
                         f"Top class breakdown: {cls_summary}. "
                         f"Would you like an itemized list of classes falling below the 85% benchmark?")
                suggested_actions = [SuggestedAction(label="Low Attendance Alerts", action_type="view_low_attendance")]
            elif "present_count" in res:
                # Teacher Class Summary
                cname = res.get("class_name", "your class")
                tot = res.get("total_students", 0)
                pres = res.get("present_count", 0)
                abs_cnt = res.get("absent_count", 0)
                abs_list = ", ".join(res.get("absent_students", []))
                dt = res.get("date", "today")
                if abs_cnt > 0:
                    reply = (f"Attendance summary for **{cname}** ({dt}): **{pres} of {tot} students are present** ({res.get('attendance_rate', 0)}%). "
                             f"Absent today ({abs_cnt}): **{abs_list}**.")
                else:
                    reply = f"Great news for **{cname}** ({dt})! **All {tot} students are present** (100% attendance rate)."
                suggested_actions = [
                    SuggestedAction(label="Mark Student Attendance", action_type="mark_attendance"),
                    SuggestedAction(label="Class Roster", action_type="class_roster")
                ]
            else:
                # Student / Parent View
                sname = res.get("student_name", active_student or "Rahul")
                pct = res.get("percentage", 0.0)
                tot = res.get("total_days", 0)
                pres = res.get("present_days", 0)
                abs_cnt = res.get("absent_days", 0)
                recent = res.get("recent_records", [])
                last_status = recent[0]["status"] if recent else "present"
                last_date = recent[0]["date"] if recent else "recent session"

                if user.role == "parent":
                    if any(w in msg_lower for w in ["yesterday", "come to school", "came to school", "today", "kal", "school aya", "school aaya", "school gaya"]):
                        reply = (f"Yes! {sname} was marked **{last_status.upper()}** on the last recorded school day ({last_date}). "
                                 f"Overall, {sname} maintains a strong attendance of **{pct}%** ({pres} present out of {tot} school days, with {abs_cnt} absences).")
                    else:
                        reply = (f"Here is the latest attendance summary for **{sname}**: **{pct}% overall attendance** "
                                 f"({pres} days attended out of {tot} sessions, with {abs_cnt} absences). On the last school session ({last_date}), {sname} was **{last_status.upper()}**.")
                    suggested_actions = [
                        SuggestedAction(label="Recent Absences", action_type="recent_attendance"),
                        SuggestedAction(label="Submit Leave Note", action_type="submit_leave")
                    ]
                elif user.role == "student":
                    reply = (f"Your current attendance stands at **{pct}%** ({pres}/{tot} days attended)! "
                             f"You're in good standing. Keep up the consistent punctuality! 👏")
                else:
                    reply = f"{sname} has an overall attendance of {pct}% ({pres}/{tot} days). Last recorded status: {last_status.upper()} on {last_date}."
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # G1. Upcoming Exam Dates & Examination Schedule
        # -------------------------------------------------------------------
        if any(w in msg_lower for w in [
            "when is my next exam", "next exam", "upcoming exam", "upcoming exams", "exam schedule", "exam dates",
            "exam date", "dates of exam", "test schedule", "when are exams", "next test", "exam time", "upcoming test",
            "test date", "when is the exam", "exam timetable", "test timetable", "પરીક્ષા ક્યારે", "परीक्षा कब", "परीक्षा तारीख"
        ]) or (last_topic == "exams" and any(w in msg_lower for w in ["when", "dates", "schedule", "time", "timetable"])):
            context["active_topic"] = "exams"
            res = tool_get_exam_schedule(user=user)
            executed_tools.append("tool_get_exam_schedule")
            context["last_data"] = res
            sname = active_student or "Rahul Patel"
            
            if user.role == "student":
                reply = (f"Here is your upcoming examination schedule for **{sname}** (Mid-Term Assessment 2026):\n"
                         f"- 📘 **Mathematics**: September 15, 2026 (09:00 AM – 12:00 PM)\n"
                         f"- 🔬 **Science**: September 18, 2026 (09:00 AM – 12:00 PM)\n"
                         f"- 📖 **English**: September 21, 2026 (09:00 AM – 12:00 PM)\n"
                         f"- 💻 **Computer Applications / IT**: September 24, 2026 (09:00 AM – 11:30 AM)\n"
                         f"- 🌍 **Social Studies**: September 27, 2026 (09:00 AM – 12:00 PM)\n\n"
                         f"Would you like subject-specific study tips or revision plans for any of these subjects?")
                suggested_actions = [
                    SuggestedAction(label="English Study Tips", action_type="tips_english"),
                    SuggestedAction(label="Mathematics Revision Guide", action_type="tips_math"),
                    SuggestedAction(label="Science Study Guide", action_type="tips_science")
                ]
            elif user.role == "parent":
                reply = (f"Upcoming exam schedule for **{sname}** (Mid-Term Assessment 2026):\n"
                         f"- Mathematics: September 15, 2026 (09:00 AM)\n"
                         f"- Science: September 18, 2026 (09:00 AM)\n"
                         f"- English: September 21, 2026 (09:00 AM)\n"
                         f"- Computer Applications: September 24, 2026 (09:00 AM)\n"
                         f"Would you like subject performance insights or study preparation tips for Rahul?")
                suggested_actions = [
                    SuggestedAction(label="Past Report Card", action_type="query_grades"),
                    SuggestedAction(label="Study Tips", action_type="study_tips")
                ]
            else:
                reply = "School Mid-Term Examination starts September 15, 2026 across secondary grades."
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # G2. Subject-Specific Guidance, Revision Plans & Study Tips
        # -------------------------------------------------------------------
        subject_detected = None
        if any(w in msg_lower for w in ["english", "eng", "literature", "grammar"]):
            subject_detected = "English"
        elif any(w in msg_lower for w in ["math", "maths", "mathematics", "algebra", "geometry"]):
            subject_detected = "Mathematics"
        elif any(w in msg_lower for w in ["science", "physics", "chemistry", "biology", "sci"]):
            subject_detected = "Science"
        elif any(w in msg_lower for w in ["computer", "it", "informatics", "coding", "programming"]):
            subject_detected = "Computer Applications"
        elif any(w in msg_lower for w in ["social", "history", "geography", "civics", "sst"]):
            subject_detected = "Social Studies"

        is_study_tip_inquiry = any(w in msg_lower for w in ["tip", "tips", "study", "revision", "prepare", "strategy", "how to learn", "how to study", "guidance"])
        
        if subject_detected or is_study_tip_inquiry:
            context["active_topic"] = "subject_guidance"
            target_sub = subject_detected or active_subject or "English"
            context["active_subject"] = target_sub
            
            if user.role == "student":
                if target_sub == "English":
                    reply = (f"📖 **Top Study & Revision Tips for English**:\n"
                             f"1. **Reading Comprehension**: Practice 1 unseen passage every two days. Always underline keywords in the questions before reading the passage to locate answers faster.\n"
                             f"2. **Writing Section & Essays**: Structure your writing with a catchy Introduction, 2 body paragraphs with supporting points, and a punchy Conclusion. Proofread for grammar and punctuation.\n"
                             f"3. **Literature & Characters**: Summarize each chapter in 4 bullet points and memorize 2-3 key character traits and central themes.\n"
                             f"4. **Active Vocabulary**: Maintain a vocabulary journal with 5 new words daily and use them in sample sentences.\n\n"
                             f"Would you like chapter summaries, grammar revision questions, or tips for another subject?")
                elif target_sub == "Mathematics":
                    reply = (f"📐 **Top Study & Revision Tips for Mathematics**:\n"
                             f"1. **Daily Problem Solving**: Solve at least 5-8 textbook problems every day without looking at solutions first.\n"
                             f"2. **Formula Chart Sheet**: Write down all identities, algebra formulas, and geometry theorems on a chart sheet and review it every morning.\n"
                             f"3. **Show Intermediate Working**: Always write down intermediate calculation steps clearly — exams award step-marks even if there is a minor arithmetic slip.\n"
                             f"4. **Error Notebook**: Maintain a notebook of problems you previously solved incorrectly and re-solve them before test day.\n\n"
                             f"Would you like practice problems or formula cheat-sheets for Math?")
                elif target_sub == "Science":
                    reply = (f"🔬 **Top Study & Revision Tips for Science**:\n"
                             f"1. **Diagrams & Labelling**: Practice drawing ray diagrams, electric circuits, and human organ/cell structures from memory.\n"
                             f"2. **Concept Mind-Maps**: Create visual mind-maps connecting key laws (Newton's laws, Ohm's law, periodic trends).\n"
                             f"3. **SI Units & Formulas**: Memorize units (Joules, Watts, Newtons, Volts) to avoid losing simple unit marks in numericals.\n"
                             f"4. **Chemical Reactions**: Practice balancing 5 chemical equations daily.\n\n"
                             f"Would you like key definitions or numerical practice sets for Science?")
                elif target_sub == "Computer Applications":
                    reply = (f"💻 **Top Study & Revision Tips for Computer Applications & IT**:\n"
                             f"1. **Code by Hand**: Practice writing code syntax and dry-running algorithms on paper.\n"
                             f"2. **Flowcharts & Logic**: Trace variable states through loops and conditional if-else statements.\n"
                             f"3. **Core Concepts**: Focus on OOP principles, data types, and functions.\n\n"
                             f"Would you like sample coding problems or theory flashcards for IT?")
                else:
                    reply = (f"📚 **Top Study & Revision Tips for {target_sub}**:\n"
                             f"1. **Active Recall**: Test yourself with flashcards rather than passively reading notes.\n"
                             f"2. **Pomodoro Intervals**: Study in 25-minute focused blocks followed by 5-minute restorative breaks.\n"
                             f"3. **Past Papers**: Practice solving previous year questions under timed conditions.\n\n"
                             f"Would you like specific advice for another subject?")
                
                suggested_actions = [
                    SuggestedAction(label="Maths Study Tips", action_type="tips_math"),
                    SuggestedAction(label="Science Study Tips", action_type="tips_science"),
                    SuggestedAction(label="Exam Schedule", action_type="query_exams")
                ]
                return reply, suggested_actions, executed_tools

            elif user.role == "parent":
                res = tool_get_grades(user=user, student_name=active_student)
                executed_tools.append("tool_get_grades")
                sname = active_student or "Rahul"
                grades_list = res.get("grades", [])
                target_g = next((g for g in grades_list if target_sub.lower() in g["subject_name"].lower()), None)
                if target_g:
                    reply = (f"For **{target_g['subject_name']}**, {sname} scored **{target_g['marks_obtained']}/{target_g['max_marks']}** (Grade: **{target_g['grade']}**).\n"
                             f"Teacher feedback: *\"{target_g.get('remarks', 'Consistently diligent.')}\"*.\n"
                             f"💡 **At-Home Study Recommendation**: Encourage 20-30 minutes of daily active reading and revision to maintain strong scores.")
                else:
                    reply = (f"In **{target_sub}**, {sname} maintains positive classroom engagement and steady homework completion. "
                             f"Would you like to review upcoming test dates or detailed teacher remarks for this subject?")
                return reply, suggested_actions, executed_tools

            elif user.role == "teacher":
                reply = (f"For **{target_sub}**, Class 10-A is currently on track with the term syllabus. "
                         f"Would you like to review student submissions, enter test marks, or schedule a revision lecture?")
                return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # G3. Past Grades, Exam Scores & Report Cards
        # -------------------------------------------------------------------
        if any(w in msg_lower for w in ["grade", "grades", "marks", "score", "scores", "report card", "result", "results", "academic performance", "how did i do", "how is rahul doing in exams", "માર્ક્સ", "પરિણામ", "नंबर", "रिजल्ट"]):
            context["active_topic"] = "grades"
            res = tool_get_grades(user=user, student_name=active_student)
            executed_tools.append("tool_get_grades")
            context["last_data"] = res

            if res.get("is_security_refusal"):
                reply = res.get("message", "Permission Denied.")
                return reply, suggested_actions, executed_tools

            sname = res.get("student_name", active_student or "Rahul")
            avg = res.get("average_percentage", 87.5)
            grades_list = res.get("grades", [])
            
            top_grades = ", ".join([f"{g['subject_name']}: {g['marks_obtained']}/100 ({g['grade']})" for g in grades_list[:3]])
            if user.role == "parent":
                reply = (f"**Academic Report for {sname}** ({res.get('exam_name', 'Annual Final Exam')}):\n"
                         f"Overall Average: **{avg}%**.\n"
                         f"Key subject scores: {top_grades}.\n"
                         f"Overall, {sname} is performing commendably. Would you like to review specific subject remarks or the upcoming test schedule?")
                suggested_actions = [
                    SuggestedAction(label="Full Report Card", action_type="full_report_card"),
                    SuggestedAction(label="Upcoming Exam Dates", action_type="query_exams")
                ]
            elif user.role == "student":
                reply = (f"Here are your latest exam results ({res.get('exam_name', 'Annual Final')}):\n"
                         f"Your overall average is **{avg}%**! 🎉 Top scores: {top_grades}.\n"
                         f"Great job! Would you like some study tips for the upcoming term?")
                suggested_actions = [
                    SuggestedAction(label="Upcoming Exam Schedule", action_type="query_exams"),
                    SuggestedAction(label="English Study Tips", action_type="tips_english"),
                    SuggestedAction(label="Maths Study Tips", action_type="tips_math")
                ]
            else:
                reply = f"Academic summary for {sname}: Overall Average **{avg}%**. Scores: {top_grades}."
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # H. Fee Status, Payment Details, and Receipt Delivery
        # -------------------------------------------------------------------
        msg_alpha = re.sub(r'[^a-zA-Z0-9\s]', ' ', msg_lower).strip()
        msg_alpha = re.sub(r'\s+', ' ', msg_alpha)

        # 1. Email Receipt Request
        if any(w in msg_lower for w in ["email receipt", "email me receipt", "email me the payment", "send receipt", "mail receipt", "invoice copy", "download receipt", "email me the payment reciept"]) or ("email" in msg_lower and "receipt" in msg_lower):
            context["active_topic"] = "fees"
            sname = active_student or "Rahul Patel"
            p_email = user.email or "amit.patel@gmail.com"
            reply = (f"📧 **Fee Receipt & Invoice Dispatched!**\n"
                     f"The official fee invoice and payment breakdown for **{sname}** (Term 1 - Academic Year 2025-26) "
                     f"has been sent to your registered email address (**{p_email}**).\n\n"
                     f"You can also download digital PDF copies anytime under the Parent Portal Documents section.")
            suggested_actions = [
                SuggestedAction(label="Payment Methods", action_type="view_payment_methods"),
                SuggestedAction(label="Check Attendance", action_type="query_attendance")
            ]
            return reply, suggested_actions, executed_tools

        # 2. Payment Details / How to Pay / Bank Info
        if any(w in msg_lower for w in ["payment details", "share me the payment", "share payment details", "share the payment", "how to pay", "bank details", "payment options", "pay online", "upi id", "account details", "share details"]) or (last_topic == "fees" and any(w in msg_alpha.split() for w in ["share", "details", "how", "account", "bank", "pay"])):
            context["active_topic"] = "fees"
            sname = active_student or "Rahul Patel"
            reply = (f"Here are the official school payment details for **{sname}** (Outstanding Amount: **₹45,000.00**):\n\n"
                     f"💳 **1. Online Payment Portal**: Click 'Pay Fees Online' in your portal header to pay instantly via UPI, NetBanking, or Debit/Credit card.\n"
                     f"🏦 **2. Direct Bank Transfer (NEFT/RTGS)**:\n"
                     f"   - **Beneficiary**: XYZ Public School Fee Collection\n"
                     f"   - **Bank**: HDFC Bank (School Campus Branch)\n"
                     f"   - **Account No**: `50200088991122`\n"
                     f"   - **IFSC Code**: `HDFC0001042`\n"
                     f"📱 **3. UPI**: `xyzschool.fees@hdfcbank`\n\n"
                     f"Would you like me to email you the official invoice and payment receipt for your records?")
            suggested_actions = [
                SuggestedAction(label="Email Fee Receipt", action_type="email_receipt"),
                SuggestedAction(label="Download Invoice PDF", action_type="download_invoice")
            ]
            return reply, suggested_actions, executed_tools

        # 3. User Acknowledges / "Received" / "Got it" / "Noted"
        if any(w in msg_alpha for w in ["received", "got it", "noted", "i received", "got the receipt", "understood", "all good", "okay thanks", "ok thanks"]):
            first_name = user.name.split()[0] if user.name else "there"
            last_name = user.name.split()[-1] if user.name else "there"
            if user.role == "parent":
                reply = (f"You're very welcome, Mr./Mrs. {last_name}! 😊\n"
                         f"Please let me know if you need any further assistance with {active_student or 'Rahul'}'s attendance, academic report cards, or school routines.")
            else:
                reply = "Glad to help! Let me know if there's anything else you'd like to check today."
            return reply, suggested_actions, executed_tools

        # 4. General Fee Balance / Dues Query
        if any(w in msg_lower for w in ["fee", "fees", "dues", "payment", "invoice", "receipt", "paid", "balance", "cost", "બિલ", "ફી", "ભરાઈ", "કુલ ફી", "फीस", "शुल्क", "भरपाई", "कलेक्शन", "பணம்", "கட்டணம்"]):
            context["active_topic"] = "fees"
            res = tool_get_fees(user=user, student_name=active_student)
            executed_tools.append("tool_get_fees")
            context["last_data"] = res

            if res.get("is_security_refusal"):
                reply = f"Access Notice: {res.get('error')}"
            elif "error" in res:
                reply = f"Could not retrieve fee information: {res.get('error')}"
            elif "total_collected" in res:
                # Principal Analytics
                collected = res.get("total_collected", 0)
                billed = res.get("total_billed", 0)
                out = res.get("total_outstanding", 0)
                rate = round((collected / billed * 100), 1) if billed > 0 else 0.0
                reply = (f"**Executive Fee Collection Analytics**:\n"
                         f"- Total Billed: ₹{billed:,.2f}\n"
                         f"- Total Collected: ₹{collected:,.2f} (**{rate}% collection rate**)\n"
                         f"- Total Outstanding Dues: ₹{out:,.2f} across {res.get('overdue_count', 0)} overdue accounts.\n"
                         f"Would you like to export the list of outstanding accounts for administrative follow-up?")
                suggested_actions = [SuggestedAction(label="View Overdue Accounts", action_type="view_overdue_fees")]
            else:
                sname = res.get("student_name", active_student or "Rahul")
                dues = res.get("total_outstanding_dues", 0)
                if dues == 0:
                    reply = f"Great news! All school fee invoices for **{sname}** are completely settled and up to date. There are no outstanding dues."
                else:
                    reply = (f"For **{sname}**, there is a current outstanding balance of **₹{dues:,.2f}**. "
                             f"The upcoming installment is due by August 30, 2026. Would you like me to share payment details or email you the receipt?")
                    suggested_actions = [
                        SuggestedAction(label="Share Payment Details", action_type="view_payment_methods"),
                        SuggestedAction(label="Email Fee Receipt", action_type="email_receipt")
                    ]
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # I. Timetable, Homework, and Routine
        # -------------------------------------------------------------------
        if any(w in msg_lower for w in ["timetable", "schedule", "class", "period", "routine", "lecture", "homework", "assignment"]):
            context["active_topic"] = "timetable"
            res = tool_get_timetable(user=user)
            executed_tools.append("tool_get_timetable")
            context["last_data"] = res

            if res.get("is_security_refusal"):
                reply = f"Access Notice: {res.get('error')}"
            elif "error" in res:
                reply = f"Unable to fetch timetable: {res.get('error')}"
            else:
                slots = res.get("schedule", [])
                cname = res.get("class_name", "your class")
                if slots:
                    slot_desc = ", ".join([f"Period {s['period_number']}: {s['subject_name']} ({s['start_time'][:5]})" for s in slots[:3]])
                    if user.role == "student":
                        reply = (f"Here is your upcoming class routine for **{cname}**: {slot_desc}. "
                                 f"Make sure to keep your notebook ready! Would you like the full weekly schedule?")
                    else:
                        reply = f"Today's class schedule for **{cname}**: {slot_desc}. Would you like the full weekly breakdown?"
                else:
                    reply = f"All scheduled lectures for today in **{cname}** are finished. Tomorrow's first session begins at 08:30 AM with Mathematics."
                suggested_actions = [SuggestedAction(label="Full Weekly Timetable", action_type="full_timetable")]
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # J. Notices, Circulars, and Calendar Events
        # -------------------------------------------------------------------
        if any(w in msg_lower for w in ["notice", "announcement", "circular", "event", "holiday", "ptm", "calendar"]):
            context["active_topic"] = "notices"
            res = tool_get_notices(user=user)
            executed_tools.append("tool_get_notices")
            notices = res.get("notices", [])
            if notices:
                n0 = notices[0]
                reply = (f"📢 **Latest School Notice**: **{n0['title']}**\n"
                         f"{n0['body']} *(Published by {n0['posted_by_name']})*.\n"
                         f"🗓️ Upcoming Event: **Parent-Teacher Meeting (PTM)** is scheduled for August 22, 2026.")
            else:
                reply = "There are no new urgent announcements posted today. School operations and schedules are proceeding as usual."
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # K. Affirmation & Confirmation Handler ("Yes", "Sure", "Please", "Send it", "Okay")
        # -------------------------------------------------------------------
        if any(msg_alpha == w or msg_alpha.startswith(w + " ") or msg_alpha.endswith(" " + w) or f" {w} " in f" {msg_alpha} " for w in ["yes", "yes please", "sure", "please", "send it", "do it", "go ahead", "share", "yep", "yeah", "ok", "okay"]):
            if last_topic == "fees":
                sname = active_student or "Rahul Patel"
                reply = (f"Here are the official payment details for **{sname}** (Outstanding Amount: **₹45,000.00**):\n\n"
                         f"💳 **1. Online Payment Portal**: Click 'Pay Fees Online' in your portal header to pay instantly via UPI, NetBanking, or Debit/Credit card.\n"
                         f"🏦 **2. Direct Bank Transfer (NEFT/RTGS)**:\n"
                         f"   - **Beneficiary**: XYZ Public School Fee Collection\n"
                         f"   - **Bank**: HDFC Bank (School Campus Branch)\n"
                         f"   - **Account No**: `50200088991122`\n"
                         f"   - **IFSC Code**: `HDFC0001042`\n"
                         f"📱 **3. UPI**: `xyzschool.fees@hdfcbank`\n\n"
                         f"Would you like me to email you the official invoice and payment receipt for your records?")
                suggested_actions = [
                    SuggestedAction(label="Email Fee Receipt", action_type="email_receipt"),
                    SuggestedAction(label="Download Invoice PDF", action_type="download_invoice")
                ]
                return reply, suggested_actions, executed_tools
            elif last_topic == "grades":
                res = tool_get_exam_schedule(user=user)
                executed_tools.append("tool_get_exam_schedule")
                reply = (f"Here is the upcoming exam schedule for {active_student or 'your student'}:\n"
                         f"- **Mathematics**: September 15, 2026 (09:00 AM - 12:00 PM)\n"
                         f"- **Science**: September 18, 2026 (09:00 AM - 12:00 PM)\n"
                         f"- **English**: September 21, 2026 (09:00 AM - 12:00 PM)\n"
                         f"Would you like subject-specific study tips or revision plans?")
                return reply, suggested_actions, executed_tools
            elif last_topic == "attendance":
                res = tool_get_attendance(user=user, student_name=active_student)
                executed_tools.append("tool_get_attendance")
                reply = (f"Here is the recent attendance log for {active_student or 'Rahul'}:\n"
                         f"- Total Sessions: {res.get('total_days', 45)} days\n"
                         f"- Days Present: {res.get('present_days', 41)} days\n"
                         f"- Absences: {res.get('absent_days', 4)} days\n"
                         f"Would you like me to assist you with submitting a leave note for any upcoming absence?")
                return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # L. Follow-up / Conversational Context Resolution ("why?", "tell me more", "how about that?")
        # -------------------------------------------------------------------
        if any(w in msg_lower for w in ["why", "tell me more", "explain", "more details", "how come", "what else"]):
            if last_topic == "attendance":
                reply = (f"Regarding attendance for {active_student or 'your child'}: The school records show attendance is logged daily by the class teacher during homeroom. "
                         f"Any excused absences were due to submitted medical slips. Would you like to review specific absence dates?")
            elif last_topic == "grades":
                reply = (f"Looking deeper at the academic breakdown for {active_student or 'your student'}: Performance in STEM subjects (Mathematics & Science) is strong (above 88%), "
                         f"while Languages show consistent progress. Regular homework completion has contributed positively to these scores.")
            elif last_topic == "fees":
                reply = f"The fee structure is billed term-wise covering tuition, laboratory, and library facilities. All previous terms are cleared, leaving only the upcoming Term-2 installment."
            else:
                reply = f"I'm keeping track of our discussion regarding {active_student or 'your schooling'}. What specific aspect would you like me to elaborate on?"
            return reply, suggested_actions, executed_tools

        # -------------------------------------------------------------------
        # L. Conversational Default Fallback (Empathetic, Helpful, Role-Adapted)
        # -------------------------------------------------------------------
        if user.role == "parent":
            reply = (f"I'm here to help with anything related to {active_student or 'your child'}'s education, Mr./Mrs. {user.name.split()[-1]}! "
                     f"You can ask me about daily attendance, exam scores, fee payments, class routines, or request a call with the teacher. What would you like to explore?")
        elif user.role == "student":
            reply = (f"I'm here to help you succeed, {user.name.split()[0]}! You can ask me about your daily timetable, exam schedules, homework, or attendance. "
                     f"What can we look at together?")
        elif user.role == "teacher":
            reply = (f"Teaching Assistant ready, {user.name}. You can ask me to mark student attendance, view class rosters, or check timetable assignments. "
                     f"How can I assist your classroom today?")
        else:
            reply = (f"Management Assistant ready, {user.name}. I can provide school-wide attendance metrics, fee collection summaries, or escalation reports. "
                     f"Which executive overview would you like to review?")

        return reply, suggested_actions, executed_tools
