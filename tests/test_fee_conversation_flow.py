"""
XYZ AI — Multi-Turn Fee Conversation & History Persistence Tests
Validates:
1. Parent fee balance inquiry
2. Follow-up affirmative responses ('Yes' -> payment details)
3. Direct 'Share me the payment details' request
4. User acknowledgement ('Received' -> warm polite response)
5. 'email me the payment reciept' delivery confirmation
6. Cross-turn database history persistence and restoration
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
from shared.database import get_conversation_history

PARENT_AMIT = UserTokenPayload(
    user_id="usr_parent_amit",
    email="amit.patel@gmail.com",
    name="Mr. Amit Patel",
    role="parent"
)

@pytest.mark.asyncio
async def test_full_fee_conversation_flow_and_persistence():
    session_id = f"sess_test_{uuid.uuid4().hex[:8]}"

    # Turn 1: User asks about fees
    r1 = await ConversationOrchestrator.process_message(
        "Tell me about his fees.",
        user=PARENT_AMIT,
        session_id=session_id
    )
    assert "45,000" in r1.response_text or "₹45,000" in r1.response_text
    assert "payment details" in r1.response_text.lower() or "receipt" in r1.response_text.lower()

    # Turn 2: User answers 'Yes.'
    r2 = await ConversationOrchestrator.process_message(
        "Yes.",
        user=PARENT_AMIT,
        session_id=session_id
    )
    assert "hdfc" in r2.response_text.lower() or "upi" in r2.response_text.lower() or "payment" in r2.response_text.lower()
    assert "50200088991122" in r2.response_text or "hdfc" in r2.response_text.lower()

    # Turn 3: User explicitly asks 'Share me the payment details.'
    r3 = await ConversationOrchestrator.process_message(
        "Share me the payment details.",
        user=PARENT_AMIT,
        session_id=session_id
    )
    assert "hdfc" in r3.response_text.lower() or "upi" in r3.response_text.lower()
    assert "xyzschool.fees@hdfcbank" in r3.response_text or "50200088991122" in r3.response_text

    # Turn 4: User acknowledges 'Received.'
    r4 = await ConversationOrchestrator.process_message(
        "Received.",
        user=PARENT_AMIT,
        session_id=session_id
    )
    assert "welcome" in r4.response_text.lower() or "glad" in r4.response_text.lower()

    # Turn 5: User requests 'email me the payment reciept'
    r5 = await ConversationOrchestrator.process_message(
        "email me the payment reciept",
        user=PARENT_AMIT,
        session_id=session_id
    )
    assert "email" in r5.response_text.lower() or "receipt" in r5.response_text.lower()
    assert "amit.patel@gmail.com" in r5.response_text or "invoice" in r5.response_text.lower()

    # Database Cross-Turn Persistence Check
    history = get_conversation_history(session_id)
    assert len(history) >= 10  # 5 user messages + 5 assistant replies
    assert any("Tell me about his fees." in m["content"] for m in history)
    assert any("email me the payment reciept" in m["content"] for m in history)
