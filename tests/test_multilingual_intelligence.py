"""
XYZ AI — Multilingual & Hinglish Conversational Intelligence Tests
Validates:
1. Hinglish intent recognition and conversational responses
2. Hindi, Gujarati, Tamil, Marathi query understanding
3. Multilingual language code propagation and response generation
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "05_xyz_ai"))

import pytest
from shared.schemas import UserTokenPayload
from agent import ConversationOrchestrator

PARENT_AMIT = UserTokenPayload(user_id="usr_parent_amit", email="amit@gmail.com", name="Mr. Amit Patel", role="parent")
STUDENT_RAHUL = UserTokenPayload(user_id="usr_student_rahul", email="rahul@school.edu", name="Rahul Patel", role="student")

@pytest.mark.asyncio
async def test_hinglish_attendance_query():
    """Validates Hinglish query: 'kya kal Rahul school aya tha' -> triggers attendance tool and responds."""
    res = await ConversationOrchestrator.process_message(
        "kya kal Rahul school aya tha",
        user=PARENT_AMIT,
        language="hinglish"
    )
    assert "attendance" in res.response_text.lower() or "absent" in res.response_text.lower() or "present" in res.response_text.lower()
    assert "tool_get_attendance" in res.executed_tools or "get_attendance" in res.executed_tools

@pytest.mark.asyncio
async def test_hinglish_grades_query():
    """Validates Hinglish query: 'Rahul ke science me kitne marks hai' -> triggers grades tool."""
    res = await ConversationOrchestrator.process_message(
        "Rahul ke science me kitne marks hai",
        user=PARENT_AMIT,
        language="hinglish"
    )
    assert "science" in res.response_text.lower() or "marks" in res.response_text.lower()
    assert "tool_get_grades" in res.executed_tools

@pytest.mark.asyncio
async def test_hinglish_fee_dues_query():
    """Validates Hinglish query: 'kya school fees baki hai' -> triggers fee tool."""
    res = await ConversationOrchestrator.process_message(
        "kya school fees baki hai",
        user=PARENT_AMIT,
        language="hinglish"
    )
    assert "tool_get_fees" in res.executed_tools
    assert "balance" in res.response_text.lower() or "due" in res.response_text.lower() or "fee" in res.response_text.lower() or "₹" in res.response_text

@pytest.mark.asyncio
async def test_hindi_attendance_query():
    """Validates pure Hindi query: 'नमस्ते! राहुल की हाजिरी कैसी है?'"""
    res = await ConversationOrchestrator.process_message(
        "नमस्ते! राहुल की हाजिरी कैसी है?",
        user=PARENT_AMIT,
        language="hi"
    )
    assert "tool_get_attendance" in res.executed_tools
    assert "उपस्थिति" in res.response_text or "राहुल" in res.response_text or "दिन" in res.response_text

@pytest.mark.asyncio
async def test_gujarati_grades_query():
    """Validates Gujarati query: 'વિજ્ઞાનમાં કેટલા માર્ક્સ આવ્યા?'"""
    res = await ConversationOrchestrator.process_message(
        "વિજ્ઞાનમાં કેટલા માર્ક્સ આવ્યા?",
        user=PARENT_AMIT,
        language="gu"
    )
    assert "tool_get_grades" in res.executed_tools or "વિજ્ઞાન" in res.response_text or "88.5" in res.response_text
    assert "ગુણ" in res.response_text or "ટકાવારી" in res.response_text or "પરિણામ" in res.response_text or "વિજ્ઞાન" in res.response_text or "સરેરાશ" in res.response_text or "માર્ક્સ" in res.response_text

@pytest.mark.asyncio
async def test_marathi_attendance_query():
    """Validates Marathi query: 'नमस्कार, राहुलची उपस्थिती किती आहे?'"""
    res = await ConversationOrchestrator.process_message(
        "नमस्कार, राहुलची उपस्थिती किती आहे?",
        user=PARENT_AMIT,
        language="mr"
    )
    assert "tool_get_attendance" in res.executed_tools
    assert "उपस्थिती" in res.response_text or "राहुल" in res.response_text or "दिवस" in res.response_text

@pytest.mark.asyncio
async def test_teacher_gujarati_attendance_query():
    """Validates Teacher Gujarati query: 'આજે કેટલા વિદ્યાર્થીઓ હાજર છે?'"""
    TEACHER_ANJALI = UserTokenPayload(user_id="usr_teacher_01", email="anjali@school.edu", name="Mrs. Anjali Verma", role="teacher", class_id="cls_10a")
    res = await ConversationOrchestrator.process_message(
        "આજે કેટલા વિદ્યાર્થીઓ હાજર છે?",
        user=TEACHER_ANJALI,
        language="gu"
    )
    assert "tool_get_attendance" in res.executed_tools
    assert "વિદ્યાર્થીઓ હાજર છે" in res.response_text or "હાજરીનો દર" in res.response_text or "સમાચાર" in res.response_text

@pytest.mark.asyncio
async def test_explicit_language_selection_command():
    """Validates user answering language question with 'Hindi.' -> sets language to Hindi and acknowledges in Hindi."""
    res = await ConversationOrchestrator.process_message(
        "Hindi.",
        user=PARENT_AMIT,
        session_id="sess_lang_sel_01"
    )
    assert res.language == "hi"
    assert "हिन्दी" in res.response_text or "नमस्ते" in res.response_text

@pytest.mark.asyncio
async def test_marathi_grades_user_exact_query():
    """Validates exact user query in Marathi: 'माझ्या मुलाचा शेवटच्या टेस्टमध्ये किती मार्क्स आले होते?'"""
    res = await ConversationOrchestrator.process_message(
        "माझ्या मुलाचा शेवटच्या टेस्टमध्ये किती मार्क्स आले होते?",
        user=PARENT_AMIT,
        language="mr"
    )
    assert res.language == "mr"
    assert "tool_get_grades" in res.executed_tools
    # Must NOT reply in English and must contain Marathi academic terms
    assert ("राहुल" in res.response_text or "गुण" in res.response_text or "अहवाल" in res.response_text or "सरासरी" in res.response_text or "मार्क्स" in res.response_text)
    assert "I'm here to help you succeed" not in res.response_text



