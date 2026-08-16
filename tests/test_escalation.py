"""
XYZ AI — Escalation State Machine Tests
Validates:
1. Multi-turn escalation triggering on dissatisfaction ("Talk to Teacher", "Contact School Management")
2. Prompting user confirmation before dispatching
3. 3-state execution (pending -> confirmed / failed)
4. No false claims of contact without mock confirmation
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

@pytest.mark.asyncio
async def test_escalation_flow_with_confirmation():
    # Turn 1: Parent expresses dissatisfaction
    res1 = await ConversationOrchestrator.process_message(
        "I am not satisfied. I want to talk to my child's teacher.",
        user=PARENT_AMIT,
        session_id="test_sess_esc_01"
    )
    # Bot asks for confirmation first
    assert "connect you with the teacher" in res1.response_text or "request a call" in res1.response_text
    assert len(res1.suggested_actions) > 0

    # Turn 2: Parent confirms ("Yes")
    res2 = await ConversationOrchestrator.process_message(
        "Yes",
        user=PARENT_AMIT,
        session_id="test_sess_esc_01"
    )
    # Bot reports confirmed status accurately
    assert "submitted to" in res2.response_text or "notification" in res2.response_text
    assert "tool_request_escalation" in res2.executed_tools

def test_escalation_failure_state_handling():
    # Simulate service failure
    res_fail = tool_request_escalation(
        user=PARENT_AMIT,
        target_entity="teacher",
        reason="Test failure condition",
        simulate_failure=True
    )
    assert res_fail["status"] == "failed"
    assert res_fail["confirmed"] is False
