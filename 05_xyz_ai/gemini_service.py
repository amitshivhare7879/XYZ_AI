"""
XYZ AI — Live Google Gemini Integration & Tool Calling Engine
Uses Google Generative AI with structured function calling, non-blocking execution, and human persona modeling.
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
import google.generativeai as genai
from config import settings
from shared.schemas import UserTokenPayload, ChatResponse, SupportedLanguage
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

logger = logging.getLogger("xyz_ai.gemini")

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL or "gemini-1.5-flash"
        # Only configure if key looks like a real Google AI key (starts with AIzaSy)
        self.is_configured = bool(self.api_key and self.api_key.startswith("AIzaSy") and len(self.api_key) > 20)

        if self.is_configured:
            try:
                genai.configure(api_key=self.api_key)
                logger.info(f"Gemini AI client configured with model: {self.model_name}")
            except Exception as e:
                logger.warning(f"Gemini configuration error: {e}")
                self.is_configured = False
        else:
            logger.info("Gemini AI API key not configured or format is mock/placeholder. Live Gemini calls disabled.")

    def build_tools(self, user: UserTokenPayload):
        """Constructs executable function definitions for Gemini tool calling."""
        def get_attendance(student_name: str = "") -> str:
            """Retrieve attendance percentage and recent records for a student."""
            res = tool_get_attendance(user=user, student_name=student_name if student_name else None)
            return json.dumps(res)

        def mark_attendance(student_name: str, status: str, date: str = "") -> str:
            """Mark daily attendance for a student (present, absent, late, or excused)."""
            res = tool_mark_attendance(user=user, student_name=student_name, status=status, date=date if date else None)
            return json.dumps(res)

        def get_grades(student_name: str = "") -> str:
            """Retrieve academic exam marks, grades, and report card."""
            res = tool_get_grades(user=user, student_name=student_name if student_name else None)
            return json.dumps(res)

        def get_exam_schedule() -> str:
            """Retrieve academic exam dates, terms, and upcoming test schedules."""
            from tools import tool_get_exam_schedule
            res = tool_get_exam_schedule(user=user)
            return json.dumps(res)

        def get_fees(student_name: str = "") -> str:
            """Retrieve fee invoice status, pending dues, or school collection analytics."""
            res = tool_get_fees(user=user, student_name=student_name if student_name else None)
            return json.dumps(res)

        def get_timetable(day_of_week: str = "") -> str:
            """Retrieve class routine, daily periods, and timetable schedule."""
            res = tool_get_timetable(user=user, day_of_week=day_of_week if day_of_week else None)
            return json.dumps(res)

        def get_notices() -> str:
            """Retrieve latest school announcements, notices, circulars, and calendar events."""
            res = tool_get_notices(user=user)
            return json.dumps(res)

        def submit_leave(start_date: str, end_date: str, reason: str, student_name: str = "") -> str:
            """Submit a student or staff leave application."""
            res = tool_submit_leave(user=user, start_date=start_date, end_date=end_date, reason=reason, student_name=student_name if student_name else None)
            return json.dumps(res)

        def request_escalation(target_entity: str, reason: str, student_name: str = "") -> str:
            """Create an escalation ticket or callback request to a teacher, management, or counselor."""
            res = tool_request_escalation(user=user, target_entity=target_entity, reason=reason, student_name=student_name if student_name else None)
            return json.dumps(res)

        def query_school_database(sql_query: str) -> str:
            """Execute any read-only SQL query across all 19 interconnected tables in the school ERP database."""
            from tools import tool_query_database
            res = tool_query_database(user=user, sql_query=sql_query)
            return json.dumps(res)

        return [
            get_attendance,
            mark_attendance,
            get_grades,
            get_exam_schedule,
            get_fees,
            get_timetable,
            get_notices,
            submit_leave,
            request_escalation,
            query_school_database
        ]

    def _sync_generate(self, model_name: str, full_system_prompt: str, tools: list, chat_history: list, message: str) -> Tuple[str, List[str]]:
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=full_system_prompt,
            tools=tools
        )
        chat = model.start_chat(enable_automatic_function_calling=True)
        # Replay history
        for turn in chat_history[-6:]:
            role = "user" if turn.get("role") == "user" else "model"
            content = turn.get("content", "")
            if content:
                try:
                    chat.history.append({"role": role, "parts": [content]})
                except Exception:
                    pass

        response = chat.send_message(message)
        executed_tools = []
        if hasattr(response, "candidates") and response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    executed_tools.append(part.function_call.name)

        return response.text, executed_tools

    async def generate_response(
        self,
        message: str,
        user: UserTokenPayload,
        system_instruction: str,
        chat_history: List[Dict[str, str]],
        language: SupportedLanguage = "en"
    ) -> Optional[Tuple[str, List[str]]]:
        """
        Executes non-blocking Gemini generation with tool calling and strict timeout.
        Returns (response_text, list_of_executed_tools) or None if not configured/failed.
        """
        if not self.is_configured:
            return None

        try:
            tools = self.build_tools(user)
            
            full_system_prompt = (
                f"{system_instruction}\n"
                f"CURRENT USER CONTEXT:\n"
                f"- Name: {user.name}\n"
                f"- Verified Role: {user.role}\n"
                f"- User ID: {user.user_id}\n"
                f"- Preferred Language: {language}\n\n"
                f"HUMAN-LIKE CONVERSATIONAL GUIDELINES:\n"
                f"1. Conversational & Persona-Driven Tone:\n"
                f"   - Behave like a natural, thoughtful human assistant. Avoid robotic, canned, or formulaic templates.\n"
                f"   - Student: Friendly, motivating Academic Assistant. Supportive peer-tutor tone.\n"
                f"   - Parent: Caring, empathetic, patient Parent Support Assistant. Reassuring tone.\n"
                f"   - Teacher: Professional, collegial, and efficient Teaching Assistant.\n"
                f"   - Principal: Executive, concise, data-informed Management Assistant.\n"
                f"2. Multi-Turn Context & Clarifications:\n"
                f"   - Remember previous questions and references across turns.\n"
                f"   - Gracefully handle user corrections ('no, I meant Math', 'actually tomorrow') without getting confused.\n"
                f"   - If user input is ambiguous or missing required details, ask clarifying questions warmly.\n"
                f"3. Multilingual & Hinglish Support:\n"
                f"   - Naturally understand English, Hindi, Gujarati, Tamil, Telugu, Marathi, Bengali, Punjabi, Kannada, Malayalam, Urdu, and Hinglish.\n"
                f"4. Real Database Integration:\n"
                f"   - Use available tools to fetch ground truth records. Never fabricate student marks or attendance."
            )

            # Run in thread with 5.0 second timeout to prevent event loop blocking
            result = await asyncio.wait_for(
                asyncio.to_thread(
                    self._sync_generate,
                    self.model_name,
                    full_system_prompt,
                    tools,
                    chat_history,
                    message
                ),
                timeout=5.0
            )
            return result
        except Exception as e:
            logger.warning(f"Live Gemini API call failed or timed out: {e}")
            return None

gemini_service = GeminiService()
