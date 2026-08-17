"""
XYZ AI — Shared Pydantic Schemas
Defines request/response models and data contracts for 05_xyz_ai backend.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import date, datetime

UserRole = Literal['student', 'parent', 'teacher', 'principal']
SupportedLanguage = Literal['en', 'hi', 'ta', 'te', 'mr', 'bn', 'gu', 'pa', 'kn', 'ml', 'ur', 'hinglish']

class UserTokenPayload(BaseModel):
    user_id: str
    email: str = "demo@school.edu"
    name: str
    role: UserRole
    preferred_language: str = 'en'

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    language: Optional[str] = None
    voice_response_requested: bool = False
    user: Optional[Dict[str, Any]] = None

class VisemeCue(BaseModel):
    time: float
    viseme: str

class SuggestedAction(BaseModel):
    label: str
    action_type: str
    payload: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response_text: str
    session_id: str
    language: SupportedLanguage
    audio_base64: Optional[str] = None
    visemes: Optional[List[VisemeCue]] = None
    suggested_actions: Optional[List[SuggestedAction]] = None
    executed_tools: Optional[List[str]] = Field(default_factory=list)

class AttendanceQuery(BaseModel):
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    class_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class MarkAttendanceRequest(BaseModel):
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    class_id: Optional[str] = None
    date: Optional[str] = None
    status: Literal['present', 'absent', 'late', 'excused']
    remarks: Optional[str] = None

class EscalationRequest(BaseModel):
    student_id: Optional[str] = None
    target_entity: Literal['teacher', 'management', 'principal', 'counselor']
    reason: str

class LeaveApplicationRequest(BaseModel):
    student_id: Optional[str] = None
    start_date: str
    end_date: str
    reason: str
