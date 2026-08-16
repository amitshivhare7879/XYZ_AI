"""
XYZ AI — FastAPI Backend Server & Gateway
Serves the 4 School ERP Portals: Student, Parent, Staff, and Management.
Enforces thin-client architecture and cryptographic JWT application-layer RBAC.
"""

import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from shared.schemas import (
    UserTokenPayload,
    ChatRequest,
    ChatResponse,
    UserRole,
    SupportedLanguage
)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from auth import (
    create_access_token,
    get_current_user,
    require_role
)
from agent import ConversationOrchestrator
from voice import process_stt_audio, generate_tts_payload
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
from shared.database import get_db_connection

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="XYZ AI — School ERP Assistant Engine",
    version="2.0.0",
    description="Human-like AI School Assistant backend for Student, Parent, Teacher, and Management portals."
)

# Enable CORS for all frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all 4 Portals & Unified Login for single-origin deployment (e.g. Hugging Face Spaces / Docker)
root_dir = Path(__file__).parent.parent
if (root_dir / "01_student_portal").exists():
    app.mount("/student", StaticFiles(directory=str(root_dir / "01_student_portal"), html=True), name="student")
if (root_dir / "02_parent_portal").exists():
    app.mount("/parent", StaticFiles(directory=str(root_dir / "02_parent_portal"), html=True), name="parent")
if (root_dir / "03_staff_portal").exists():
    app.mount("/staff", StaticFiles(directory=str(root_dir / "03_staff_portal"), html=True), name="staff")
if (root_dir / "04_management_portal").exists():
    app.mount("/management", StaticFiles(directory=str(root_dir / "04_management_portal"), html=True), name="management")
if (root_dir / "unified_login").exists():
    app.mount("/login", StaticFiles(directory=str(root_dir / "unified_login"), html=True), name="login")

from fastapi.responses import FileResponse, Response

@app.get("/")
def serve_root():
    login_path = root_dir / "unified_login" / "index.html"
    if login_path.exists():
        return FileResponse(str(login_path))
    return {"message": "XYZ AI School ERP Engine Online", "docs": "/docs"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

# Mock demo accounts for quick role-switching
DEMO_ACCOUNTS = {
    "student": UserTokenPayload(
        user_id="usr_student_rahul",
        email="rahul.patel@student.school.edu",
        name="Rahul Patel",
        role="student",
        preferred_language="en"
    ),
    "parent": UserTokenPayload(
        user_id="usr_parent_amit",
        email="amit.patel@gmail.com",
        name="Mr. Amit Patel",
        role="parent",
        preferred_language="en"
    ),
    "teacher": UserTokenPayload(
        user_id="usr_teacher_01",
        email="anjali.verma@school.edu",
        name="Mrs. Anjali Verma",
        role="teacher",
        preferred_language="en"
    ),
    "principal": UserTokenPayload(
        user_id="usr_principal_01",
        email="principal@school.edu",
        name="Dr. Rajesh Sharma",
        role="principal",
        preferred_language="en"
    )
}

class EmailPasswordLoginRequest(BaseModel):
    email: str
    password: Optional[str] = "password123"

class LoginRequest(BaseModel):
    role: UserRole = "parent"
    custom_user_id: Optional[str] = None
    language: Optional[SupportedLanguage] = "en"

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserTokenPayload

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "XYZ AI Core Engine",
        "version": "2.0.0",
        "gemini_ai_configured": bool(os.getenv("GEMINI_API_KEY")),
        "supabase_configured": bool(os.getenv("SUPABASE_URL"))
    }

# 1A. Standard Email/Password Auth Login
@app.post("/api/auth/login", response_model=LoginResponse)
def login_with_credentials(req: EmailPasswordLoginRequest):
    """Authenticates a user via email and returns a signed JWT."""
    email_clean = req.email.strip().lower()

    # 1. Immediate demo account fast-path
    for role_name, demo_user in DEMO_ACCOUNTS.items():
        if demo_user.email.lower() == email_clean:
            token = create_access_token(demo_user)
            return LoginResponse(access_token=token, user=demo_user)

    # 2. Database lookup (SQLite or Supabase PostgreSQL)
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id, auth_id, email, name, role, preferred_language FROM users WHERE LOWER(email) = LOWER(?)", (email_clean,))
        user_row = c.fetchone()
        conn.close()

        if user_row:
            user_payload = UserTokenPayload(
                user_id=user_row["id"],
                email=user_row["email"],
                name=user_row["name"],
                role=user_row["role"],
                preferred_language=user_row["preferred_language"] or "en"
            )
            token = create_access_token(user_payload)
            return LoginResponse(access_token=token, user=user_payload)
    except Exception as e:
        print(f"[Auth Warning] Database lookup error: {e}")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"User with email '{req.email}' not found in school directory."
    )

# 1B. Quick Role Switcher Auth Endpoint
@app.post("/api/auth/mock-login", response_model=LoginResponse)
def mock_login(req: LoginRequest):
    """Generates a cryptographic JWT token for quick role testing."""
    user_payload = DEMO_ACCOUNTS.get(req.role)
    if not user_payload:
        raise HTTPException(status_code=400, detail="Invalid role specified")

    if req.language:
        user_payload.preferred_language = req.language

    token = create_access_token(user_payload)
    return LoginResponse(access_token=token, user=user_payload)

@app.get("/api/auth/me", response_model=UserTokenPayload)
def get_current_user_profile(user: UserTokenPayload = Depends(get_current_user)):
    """Returns the verified claims of the calling user."""
    return user

# 2. Main Conversational Chat Endpoint (Core Requirement)
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    req: ChatRequest,
    user: UserTokenPayload = Depends(get_current_user)
):
    """
    Main AI conversation endpoint.
    Orchestrates 4 personas, application-layer RBAC, slot filling, and 11-language generation.
    """
    return await ConversationOrchestrator.process_message(
        message=req.message,
        user=user,
        session_id=req.session_id,
        language=req.language,
        voice_requested=req.voice_response_requested
    )

# 3. Voice Pipeline Endpoints
@app.post("/api/voice/transcribe")
async def transcribe_audio_endpoint(
    file: UploadFile = File(...),
    user: UserTokenPayload = Depends(get_current_user)
):
    """Transcribes audio recordings to text via STT."""
    content = await file.read()
    text = process_stt_audio(content, filename=file.filename or "audio.webm")
    return {"transcript": text}

@app.post("/api/voice/synthesize")
def synthesize_speech_endpoint(
    text: str = Form(...),
    language: SupportedLanguage = Form("en"),
    user: UserTokenPayload = Depends(get_current_user)
):
    """Synthesizes speech metadata and viseme stream for 3D avatar."""
    return generate_tts_payload(text, language=language)

# 4. Direct ERP REST API Endpoints (Thin-client portal support)

@app.get("/api/erp/attendance/summary")
def get_attendance_summary_endpoint(
    student_name: Optional[str] = None,
    user: UserTokenPayload = Depends(get_current_user)
):
    res = tool_get_attendance(user=user, student_name=student_name)
    if res.get("is_security_refusal"):
        raise HTTPException(status_code=403, detail=res.get("error"))
    return res

@app.post("/api/erp/attendance/mark")
def mark_attendance_endpoint(
    student_name: str,
    status: str,
    date: Optional[str] = None,
    remarks: Optional[str] = None,
    user: UserTokenPayload = Depends(require_role("teacher", "principal"))
):
    res = tool_mark_attendance(user=user, student_name=student_name, status=status, date=date, remarks=remarks)
    if res.get("is_security_refusal"):
        raise HTTPException(status_code=403, detail=res.get("error"))
    if "error" in res:
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res

@app.get("/api/erp/academics/grades")
def get_grades_endpoint(
    student_name: Optional[str] = None,
    user: UserTokenPayload = Depends(get_current_user)
):
    res = tool_get_grades(user=user, student_name=student_name)
    if res.get("is_security_refusal"):
        raise HTTPException(status_code=403, detail=res.get("error"))
    return res

@app.get("/api/erp/fees/status")
def get_fees_endpoint(
    student_name: Optional[str] = None,
    user: UserTokenPayload = Depends(require_role("parent", "principal"))
):
    res = tool_get_fees(user=user, student_name=student_name)
    if res.get("is_security_refusal"):
        raise HTTPException(status_code=403, detail=res.get("error"))
    return res

@app.get("/api/erp/timetable")
def get_timetable_endpoint(
    day: Optional[str] = None,
    user: UserTokenPayload = Depends(get_current_user)
):
    res = tool_get_timetable(user=user, day_of_week=day)
    if res.get("is_security_refusal"):
        raise HTTPException(status_code=403, detail=res.get("error"))
    return res

@app.get("/api/erp/notices")
def get_notices_endpoint(user: UserTokenPayload = Depends(get_current_user)):
    return tool_get_notices(user=user)

@app.post("/api/erp/escalation/request")
def create_escalation_endpoint(
    target_entity: str,
    reason: str,
    student_name: Optional[str] = None,
    user: UserTokenPayload = Depends(get_current_user)
):
    res = tool_request_escalation(user=user, target_entity=target_entity, reason=reason, student_name=student_name)
    if res.get("is_security_refusal"):
        raise HTTPException(status_code=403, detail=res.get("error"))
    return res

@app.get("/api/erp/escalation/tickets")
def list_escalation_tickets(user: UserTokenPayload = Depends(require_role("principal", "teacher"))):
    """Retrieves school escalation queue for management."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT e.id, e.requested_by_role, e.target_entity, e.target_user_id, e.reason, e.status, e.created_at,
               u.name as requester_name, s.name as student_name
        FROM escalation_tickets e
        JOIN users u ON u.id = e.requested_by_user_id
        LEFT JOIN students s ON s.id = e.student_id
        ORDER BY e.created_at DESC
    """)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("05_xyz_ai.main:app", host="0.0.0.0", port=8000, reload=True)
