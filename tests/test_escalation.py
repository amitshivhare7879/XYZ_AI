"""
XYZ AI — Escalation State Machine Tests
Validates:
1. Multi-turn escalation triggering on dissatisfaction ("Talk to Teacher", "Contact School Management")
2. Prompting user confirmation before dispatching mock service
3. Exact dialogue matching the specification:
   - Parent: "I am not satisfied. I want to talk to my child's teacher."
   - XYZ AI: "Of course. I can connect you with the teacher. Would you like me to request a call now?"
   - Parent: "Yes."
   - XYZ AI: "Your call request has been submitted to the teacher."
4. Contact School Management escalation flow
5. 3-state execution (pending -> confirmed / failed)
6. Guaranteed safety: Never claims teacher/management is contacted unless confirmed by mock service
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "05_xyz_ai"))

import pytest
from shared.schemas import UserTokenPayload
from agent import ConversationOrchestrator
from tools import tool_request_escalation

PARENT_AMIT = UserTokenPayload(user_id="usr_parent_amit", email="amit@gmail.com", name="Mr. Amit Patel", role="parent")
STUDENT_RAHUL = UserTokenPayload(user_id="usr_student_rahul", email="rahul@school.edu", name="Rahul Patel", role="student")

@pytest.mark.asyncio
async def test_escalation_teacher_call_flow():
    """
    Validates exact specification flow:
    Parent: 'I am not satisfied. I want to talk to my child's teacher.'
    XYZ AI: 'Of course. I can connect you with the teacher. Would you like me to request a call now?'
    Parent: 'Yes.'
    XYZ AI: 'Your call request has been submitted to the teacher.'
    """
    sid = "test_sess_esc_teacher_01"
    
    # Turn 1: Parent expresses dissatisfaction and requests teacher
    res1 = await ConversationOrchestrator.process_message(
        "I am not satisfied. I want to talk to my child's teacher.",
        user=PARENT_AMIT,
        session_id=sid
    )
    # Check confirmation prompt
    assert "connect you with the teacher" in res1.response_text
    assert "request a call" in res1.response_text
    # Check provided options
    action_labels = [a.label for a in res1.suggested_actions]
    assert "Talk to Teacher" in action_labels
    assert "Contact School Management" in action_labels

    # Turn 2: Parent confirms ("Yes")
    res2 = await ConversationOrchestrator.process_message(
        "Yes",
        user=PARENT_AMIT,
        session_id=sid
    )
    # Check confirmed submission
    assert "call request has been submitted to the teacher" in res2.response_text
    assert "tool_request_escalation" in res2.executed_tools

@pytest.mark.asyncio
async def test_escalation_school_management_flow():
    """
    Validates escalation to School Management:
    User: 'Contact School Management'
    XYZ AI: 'Of course. I can connect you with School Management. Would you like me to submit a support request now?'
    User: 'Yes'
    XYZ AI: 'Your support request has been submitted to School Management. Ticket ID #...'
    """
    sid = "test_sess_esc_mgmt_01"
    
    # Turn 1: User requests School Management
    res1 = await ConversationOrchestrator.process_message(
        "I have a complaint, connect me to school management",
        user=PARENT_AMIT,
        session_id=sid
    )
    assert "connect you with school management" in res1.response_text.lower()
    
    # Turn 2: User confirms
    res2 = await ConversationOrchestrator.process_message(
        "Yes, please submit",
        user=PARENT_AMIT,
        session_id=sid
    )
    assert "submitted to school management" in res2.response_text.lower()
    assert "tool_request_escalation" in res2.executed_tools

@pytest.mark.asyncio
async def test_student_escalation_flow():
    """Validates student escalation offers 'Talk to Teacher' and 'Contact School Management'."""
    sid = "test_sess_esc_student"
    res1 = await ConversationOrchestrator.process_message(
        "I need human assistance, can I speak to someone?",
        user=STUDENT_RAHUL,
        session_id=sid
    )
    action_labels = [a.label for a in res1.suggested_actions]
    assert "Talk to Teacher" in action_labels
    assert "Contact School Management" in action_labels

def test_escalation_failure_state_handling():
    """Validates that simulated dispatch failure marks confirmed=False and never falsely claims contact."""
    res_fail = tool_request_escalation(
        user=PARENT_AMIT,
        target_entity="teacher",
        reason="Network timeout test",
        simulate_failure=True
    )
    assert res_fail["status"] == "failed"
    assert res_fail["confirmed"] is False
