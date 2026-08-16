# 05. XYZ AI — Core Engine & Backend

The `05_xyz_ai` module is the single backend and security boundary for the entire School ERP Ecosystem.

## Architecture
- **FastAPI Engine**: Serves chat, voice, authentication, and REST ERP endpoints.
- **Application-Layer RBAC (`rbac.py`)**: Deterministic permission matrix and entity ownership validation (`parent_student_links`, `teacher_class_links`) in Python code before any tool execution.
- **Conversational Orchestrator (`agent.py`)**:
  - 4 AI Personas: Student, Parent, Teacher, Principal.
  - Multi-turn conversation memory with slot filling and ambiguity detection.
  - 3-State Escalation Guarantee (`pending` → `confirmed` / `failed`).
  - 11 Indian Languages support.
- **Voice Pipeline (`voice.py`)**: Speech-To-Text audio transcription and Text-To-Speech with ARKit viseme timeline calculation.
- **ERP Services (`erp_services.py`)**: Mock database query implementations across Attendance, Academics, Fees, Timetables, Notices, Leave, and Escalations.

## Running the Backend
```bash
python -m uvicorn 05_xyz_ai.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive OpenAPI Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
