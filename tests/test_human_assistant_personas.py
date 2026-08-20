"""
XYZ AI — Automated Test Suite for Human-Like AI Personas & Conversational Intelligence
Tests:
1. Natural greetings and tone adaptation across all 4 Personas:
   - Student (Friendly, supportive Academic Assistant)
   - Parent (Caring, patient Parent Support Assistant)
   - Teacher (Professional Teaching Assistant)
   - Principal (Professional Management Assistant)
2. Multi-turn dialogue memory and context retention
3. Conversational corrections (e.g., subject change, attendance status correction)
4. Follow-up question resolution ("why?", "tell me more", "how is he doing?")
5. Clarification questions (e.g., leave requests without dates/reasons)
6. Emotional/empathy adaptation (student exam stress, parent gratitude)
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "05_xyz_ai"))

import pytest
from shared.schemas import UserTokenPayload
from agent import ConversationOrchestrator, SESSION_MEMORY

STUDENT_RAHUL = UserTokenPayload(user_id="usr_student_rahul", email="rahul@school.edu", name="Rahul Patel", role="student")
PARENT_AMIT = UserTokenPayload(user_id="usr_parent_amit", email="amit@gmail.com", name="Mr. Amit Patel", role="parent")
TEACHER_ANJALI = UserTokenPayload(user_id="usr_teacher_01", email="anjali@school.edu", name="Mrs. Anjali Verma", role="teacher")
PRINCIPAL_SHARMA = UserTokenPayload(user_id="usr_principal_01", email="principal@school.edu", name="Dr. Rajesh Sharma", role="principal")


# ---------------------------------------------------------------------------
# Test 1: Persona-Specific Natural Greetings & Tone
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_student_persona_greeting():
    """Student receives a friendly, encouraging academic assistant greeting."""
    res = await ConversationOrchestrator.process_message("Hi there!", user=STUDENT_RAHUL, session_id="sess_stu_greet")
    text = res.response_text.lower()
    assert any(w in text for w in ["hey", "good morning", "good afternoon", "good evening", "academic assistant", "studies", "timetable", "homework", "language"])
    assert "rahul" in text
    assert len(SESSION_MEMORY["sess_stu_greet"]["messages"]) >= 2

@pytest.mark.asyncio
async def test_parent_persona_greeting():
    """Parent receives a warm, caring, patient parent support assistant greeting."""
    res = await ConversationOrchestrator.process_message("Good morning", user=PARENT_AMIT, session_id="sess_par_greet")
    text = res.response_text.lower()
    assert any(w in text for w in ["parent support assistant", "rahul", "child", "assist", "progress", "attendance", "language"])
    assert "patel" in text or "amit" in text

@pytest.mark.asyncio
async def test_teacher_persona_greeting():
    """Teacher receives a professional, collegial teaching assistant greeting."""
    res = await ConversationOrchestrator.process_message("Hello", user=TEACHER_ANJALI, session_id="sess_tch_greet")
    text = res.response_text.lower()
    assert any(w in text for w in ["teaching assistant", "attendance", "roster", "assist", "language"])
    assert "anjali" in text or "verma" in text

@pytest.mark.asyncio
async def test_principal_persona_greeting():
    """Principal receives an executive, management assistant greeting."""
    res = await ConversationOrchestrator.process_message("Good morning", user=PRINCIPAL_SHARMA, session_id="sess_prn_greet")
    text = res.response_text.lower()
    assert any(w in text for w in ["management assistant", "attendance", "metrics", "fee", "escalation", "leadership", "athena", "language"])
    assert "sharma" in text or "rajesh" in text


# ---------------------------------------------------------------------------
# Test 2: Multi-Turn Conversation Memory & Context Retention
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_multi_turn_context_memory():
    """Verify that context (active student, topic, subject) is retained across turns."""
    import uuid
    sid = f"sess_multi_turn_{uuid.uuid4().hex[:8]}"
    
    # Turn 1: Parent asks about attendance
    res1 = await ConversationOrchestrator.process_message("How is my child's attendance?", user=PARENT_AMIT, session_id=sid)
    assert "Rahul" in res1.response_text
    assert "%" in res1.response_text or "attendance" in res1.response_text.lower()
    
    # Turn 2: Follow-up question relying on prior context ("why?" or "tell me more")
    res2 = await ConversationOrchestrator.process_message("Can you tell me more details about that?", user=PARENT_AMIT, session_id=sid)
    assert "attendance" in res2.response_text.lower() or "rahul" in res2.response_text.lower()
    
    # Turn 3: Topic switch to grades
    res3 = await ConversationOrchestrator.process_message("What about his grades?", user=PARENT_AMIT, session_id=sid)
    assert "grade" in res3.response_text.lower() or "score" in res3.response_text.lower() or "%" in res3.response_text
    
    # Check session memory has full conversation history
    assert len(SESSION_MEMORY[sid]["messages"]) == 6


# ---------------------------------------------------------------------------
# Test 3: Handling Conversational Corrections
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_subject_correction_handling():
    """User corrects the subject in dialogue (e.g. 'No, I meant Science')."""
    sid = "sess_correction_01"
    
    # Turn 1: Parent queries grades
    await ConversationOrchestrator.process_message("Check Rahul's grades", user=PARENT_AMIT, session_id=sid)
    
    # Turn 2: Parent corrects to a specific subject
    res2 = await ConversationOrchestrator.process_message("No, I meant for Science specifically", user=PARENT_AMIT, session_id=sid)
    assert "Science" in res2.response_text
    assert "/100" in res2.response_text or "grade" in res2.response_text.lower() or "score" in res2.response_text.lower()


# ---------------------------------------------------------------------------
# Test 4: Clarification Questions for Underspecified Requests
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_leave_clarification_question():
    """When a parent asks for leave without dates or reasons, AI asks clarifying questions."""
    sid = "sess_leave_clarify"
    res = await ConversationOrchestrator.process_message("I need to apply for leave for my child", user=PARENT_AMIT, session_id=sid)
    text = res.response_text.lower()
    # Should ask for dates and reason politely
    assert any(w in text for w in ["date", "reason", "absence", "share"])
    assert "rahul" in text or "child" in text


# ---------------------------------------------------------------------------
# Test 5: Follow-Up Holistic Inquiries ("How is my child doing?")
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_holistic_child_status_inquiry():
    """Parent asks broad conversational question 'How is he doing?'"""
    sid = "sess_holistic"
    res = await ConversationOrchestrator.process_message("How is Rahul doing in school lately?", user=PARENT_AMIT, session_id=sid)
    text = res.response_text.lower()
    assert "rahul" in text
    assert "attendance" in text
    assert "average" in text or "marks" in text or "grades" in text


# ---------------------------------------------------------------------------
# Test 6: Emotional & Sentiment Adaptation
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_student_stress_empathy():
    """Student expresses anxiety/stress about upcoming exams, AI responds with supportive empathy."""
    sid = "sess_stress"
    res = await ConversationOrchestrator.process_message("I'm feeling really stressed about my upcoming exams", user=STUDENT_RAHUL, session_id=sid)
    text = res.response_text.lower()
    assert any(w in text for w in ["understand", "normal", "breath", "break", "together", "exam schedule", "plan"])

@pytest.mark.asyncio
async def test_parent_gratitude_response():
    """Parent says thank you, AI responds with polite, caring warmth."""
    sid = "sess_thanks"
    res = await ConversationOrchestrator.process_message("Thank you so much for your help!", user=PARENT_AMIT, session_id=sid)
    text = res.response_text.lower()
    assert any(w in text for w in ["pleasure", "welcome", "assist", "wonderful day", "anytime"])
