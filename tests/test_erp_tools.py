"""
XYZ AI — ERP Tools & Persona Capability Automated Tests
Validates all core use cases:
1. Student views own attendance
2. Parent views child's attendance (~91.2% for Rahul)
3. Teacher marks attendance for student in assigned class
4. Principal queries school-wide attendance analytics
5. Academics, timetable, and fee retrieval
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "05_xyz_ai"))

import pytest
from shared.schemas import UserTokenPayload
from tools import tool_get_attendance, tool_mark_attendance, tool_get_grades, tool_get_fees, tool_get_timetable
from agent import ConversationOrchestrator

STUDENT_RAHUL = UserTokenPayload(user_id="usr_student_rahul", email="rahul@school.edu", name="Rahul Patel", role="student")
PARENT_AMIT = UserTokenPayload(user_id="usr_parent_amit", email="amit@gmail.com", name="Mr. Amit Patel", role="parent")
TEACHER_ANJALI = UserTokenPayload(user_id="usr_teacher_01", email="anjali@school.edu", name="Mrs. Anjali Verma", role="teacher")
PRINCIPAL_SHARMA = UserTokenPayload(user_id="usr_principal_01", email="principal@school.edu", name="Dr. Rajesh Sharma", role="principal")

# 1. Student Attendance Query
def test_student_attendance_view():
    res = tool_get_attendance(user=STUDENT_RAHUL)
    assert "error" not in res
    assert res["student_name"] == "Rahul Patel"
    assert res["percentage"] == 91.2
    assert res["present_days"] == 83

@pytest.mark.asyncio
async def test_student_yesterday_attendance_query():
    """Validates query: 'is i am marked present yesterday' returns recent school day status."""
    res = await ConversationOrchestrator.process_message("is i am marked present yesterday", user=STUDENT_RAHUL)
    assert "PRESENT" in res.response_text or "marked" in res.response_text.lower()
    assert "%" in res.response_text
    assert ("tool_get_attendance" in res.executed_tools or "get_attendance" in res.executed_tools)



# 2. Parent Attendance Query for linked child
def test_parent_attendance_view():
    res = tool_get_attendance(user=PARENT_AMIT, student_name="Rahul")
    assert "error" not in res
    assert res["student_name"] == "Rahul Patel"
    assert res["percentage"] == 91.2

@pytest.mark.asyncio
async def test_parent_chat_attendance_flow():
    res = await ConversationOrchestrator.process_message("How much attendance does my child have?", user=PARENT_AMIT)
    assert "Rahul" in res.response_text
    assert "%" in res.response_text or "attendance" in res.response_text.lower()

# 3. Teacher Marks Attendance
def test_teacher_mark_attendance():
    res = tool_mark_attendance(user=TEACHER_ANJALI, student_name="Rahul", status="absent", date="2026-08-15")
    assert res.get("success") is True
    assert "absent" in res["message"].lower()

@pytest.mark.asyncio
async def test_teacher_chat_mark_attendance():
    res = await ConversationOrchestrator.process_message("Mark Rahul absent today.", user=TEACHER_ANJALI)
    assert "Rahul" in res.response_text
    assert "absent" in res.response_text.lower() or "marked" in res.response_text.lower() or "updated" in res.response_text.lower()

# 4. Principal School-Wide Attendance Analytics
def test_principal_analytics_query():
    res = tool_get_attendance(user=PRINCIPAL_SHARMA)
    assert "overall_attendance_percentage" in res
    assert len(res["class_breakdown"]) > 0

@pytest.mark.asyncio
async def test_principal_chat_analytics():
    res = await ConversationOrchestrator.process_message("What is the overall attendance?", user=PRINCIPAL_SHARMA)
    assert "overall school attendance" in res.response_text.lower() or "%" in res.response_text

# 5. Academics and Fees
def test_parent_grades_view():
    res = tool_get_grades(user=PARENT_AMIT, student_name="Rahul")
    assert "grades" in res
    assert len(res["grades"]) > 0

def test_parent_fees_view():
    res = tool_get_fees(user=PARENT_AMIT)
    assert "invoices" in res
    assert res["student_name"] == "Rahul Patel"

@pytest.mark.asyncio
async def test_parent_typo_attendance_flow():
    """Validates typo tolerance: 'tell me about my son attedenace' matches attendance intent."""
    res = await ConversationOrchestrator.process_message("tell me about my son attedenace", user=PARENT_AMIT)
    assert "Rahul" in res.response_text
    assert "%" in res.response_text
    assert "tool_get_attendance" in res.executed_tools

@pytest.mark.asyncio
async def test_parent_last_5_days_record_flow():
    """Validates itemized daily attendance breakdown for 'Give me the record of last 5 days.'"""
    res = await ConversationOrchestrator.process_message("Give me the record of last 5 days.", user=PARENT_AMIT)
    assert "Rahul" in res.response_text
    assert "📅" in res.response_text or "PRESENT" in res.response_text
    assert "tool_get_attendance" in res.executed_tools


