"""
XYZ AI — Student Exam Schedule, Subject Guidance & Multi-Turn Study Flow Tests
Validates:
1. Student attendance query
2. 'When is my next exam?' returns upcoming dates, NOT past report cards
3. Subject study tips when student replies with 'english', 'mathematics', or 'science'
4. Universal role-adapted subject response logic
"""

import sys
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "05_xyz_ai"))

import pytest
from shared.schemas import UserTokenPayload
from agent import ConversationOrchestrator

STUDENT_RAHUL = UserTokenPayload(
    user_id="usr_student_rahul",
    email="rahul.patel@student.school.edu",
    name="Rahul Patel",
    role="student"
)

PARENT_AMIT = UserTokenPayload(
    user_id="usr_parent_amit",
    email="amit.patel@gmail.com",
    name="Mr. Amit Patel",
    role="parent"
)

@pytest.mark.asyncio
async def test_student_next_exam_and_english_study_tips_flow():
    session_id = f"sess_student_{uuid.uuid4().hex[:8]}"

    # Turn 1: Attendance
    r1 = await ConversationOrchestrator.process_message(
        "What is my attendance?",
        user=STUDENT_RAHUL,
        session_id=session_id
    )
    assert "91.2" in r1.response_text or "83" in r1.response_text
    assert "tool_get_attendance" in r1.executed_tools

    # Turn 2: 'When is my next exam?' -> MUST return upcoming schedule, not past marks
    r2 = await ConversationOrchestrator.process_message(
        "When is my next exam?",
        user=STUDENT_RAHUL,
        session_id=session_id
    )
    assert "september" in r2.response_text.lower() or "mathematics" in r2.response_text.lower()
    assert "english" in r2.response_text.lower()
    assert "tool_get_exam_schedule" in r2.executed_tools

    # Turn 3: Student responds with 'english'
    r3 = await ConversationOrchestrator.process_message(
        "english",
        user=STUDENT_RAHUL,
        session_id=session_id
    )
    assert "comprehension" in r3.response_text.lower() or "essay" in r3.response_text.lower() or "vocabulary" in r3.response_text.lower()
    assert "english" in r3.response_text.lower()

    # Turn 4: Student asks for 'mathematics' tips
    r4 = await ConversationOrchestrator.process_message(
        "mathematics",
        user=STUDENT_RAHUL,
        session_id=session_id
    )
    assert "problem" in r4.response_text.lower() or "formula" in r4.response_text.lower()
    assert "mathematics" in r4.response_text.lower() or "math" in r4.response_text.lower()

@pytest.mark.asyncio
async def test_parent_subject_inquiry():
    session_id = f"sess_parent_sub_{uuid.uuid4().hex[:8]}"
    r = await ConversationOrchestrator.process_message(
        "How is Rahul doing in science?",
        user=PARENT_AMIT,
        session_id=session_id
    )
    assert "science" in r.response_text.lower()
    assert "tool_get_grades" in r.executed_tools
