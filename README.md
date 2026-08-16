---
title: XYZ AI School ERP
emoji: 🎓
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 4.19.2
app_file: app.py
pinned: false
---

# XYZ AI — Human-Like AI School Assistant Ecosystem

**XYZ AI** is an Applied AI solution that functions as a real human school assistant for **Students, Parents, Teachers, and School Leadership/Principal** across **Chat, Voice, and 3D AI Avatars**.

Built on a strict **monorepo architecture**, it enforces deterministic **application-layer RBAC security**, supports **11 Indian languages**, features a **3-state honest human escalation workflow**, and encompasses full School ERP operations beyond attendance.

---

## 🏛️ Ecosystem Architecture

```
XYZ_AI/
├── 01_student_portal/      (Student Hub — Academic Assistant, Timetable, Homework, 3D Avatar)
├── 02_parent_portal/       (Parent Hub — Multi-child switcher, Attendance Insights, Fee Dues, Escalations)
├── 03_staff_portal/        (Staff/Teacher Hub — Class Roster, Voice Attendance Marker, Grade Review)
├── 04_management_portal/   (Principal Hub — School-wide Analytics, Fee Recovery, Live Escalation Queue)
├── 05_xyz_ai/              (FastAPI Backend — AI Orchestrator, RBAC Gateway, STT/TTS, Mock ERP APIs)
├── shared/                 (Postgres/SQLite Database Engine, 50+ Students Seed Data, Type Contracts)
└── tests/                  (Pytest automated test suites for RBAC security, ERP tools & Escalation)
```

> **Strict Thin-Client Boundary**: None of the 4 portal frontends access the database or LLM keys directly. Every action, mutation, query, and audio stream is signed and routed through `05_xyz_ai` using cryptographic JWT tokens.

---

## 🚀 Quickstart & Running Locally

### 1. Install Backend Dependencies
```bash
python -m pip install -r 05_xyz_ai/requirements.txt
```

### 2. Seed Mock Database (50+ Students, 10 Teachers, 40 Parents)
```bash
python -m shared.seed_data
```

### 3. Run Automated Security & ERP Test Suite (17 Tests)
```bash
python -m pytest tests/ -o asyncio_mode=auto
```

### 4. Launch All 5 Services in One Command
```bash
python start_all.py
```

### Portal URLs:
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Student Portal**: [http://localhost:3001](http://localhost:3001)
- **Parent Portal**: [http://localhost:3002](http://localhost:3002)
- **Staff / Teacher Portal**: [http://localhost:3003](http://localhost:3003)
- **Management / Principal Portal**: [http://localhost:3004](http://localhost:3004)

---

## 🛡️ Security & RBAC Enforcement (6-Threat Defense)

| Threat Vector | Defense Mechanism | Enforced Where |
|---|---|---|
| **Prompt Injection** | Structured typed schemas only; tool returns are treated as raw data variables, never executed as new instructions. | `05_xyz_ai/tools.py` |
| **Unauthorized Data Access** | Deterministic RBAC matrix + Entity Ownership joins (`parent_student_links`, `teacher_class_links`). | `05_xyz_ai/rbac.py` + DB RLS |
| **System-Prompt Extraction** | Refusal policy filters out meta instructions; secrets never exist in prompt context. | `05_xyz_ai/agent.py` |
| **API Key / Credential Leak** | Secrets reside exclusively in server environment variables. | Outside LLM context |
| **Fake Role Claims** | Role is resolved exclusively from cryptographic JWT claims; chat text like *"I am Principal"* has zero effect. | `05_xyz_ai/auth.py` |
| **Unauthorized Mutations** | Write-operations require role permission and write an immutable security audit event. | `audit_log` in DB |

---

## 🗣️ Voice, 3D Avatar & 11-Language Support

- **Speech-To-Text (STT)**: Web Speech API with backend Whisper fallback.
- **Text-To-Speech (TTS)**: Neural speech generation with ARKit/Oculus viseme timestamps.
- **3D Avatar**: Real-time facial blendshapes (mouth lip sync, eye blinks) dynamically rendered on HTML5 Canvas / Three.js.
- **11 Supported Languages**:
  1. English (`en`)
  2. Hindi (`hi`)
  3. Tamil (`ta`)
  4. Telugu (`te`)
  5. Marathi (`mr`)
  6. Bengali (`bn`)
  7. Gujarati (`gu`)
  8. Punjabi (`pa`)*
  9. Kannada (`kn`)
  10. Malayalam (`ml`)
  11. Urdu (`ur`)*

*(Note: Free neural TTS voice coverage is thinner for Punjabi & Urdu regional synthesis; text responses are 100% localized).*

---

## 📞 3-State Honest Escalation Flow

XYZ AI never claims a teacher or administrator has been contacted unless confirmed by the dispatch service:
1. **User asks for human / expresses dissatisfaction** → Bot offers explicit options (*"Talk to Teacher"*, *"Contact Management"*).
2. **User confirms** → Ticket created as `pending`, dispatched asynchronously.
3. **Dispatch outcome**:
   - `confirmed` → Bot announces: *"Your call request has been submitted to the teacher."*
   - `failed` → Bot reports: *"Unable to submit request right now — would you like to retry or receive direct contact numbers?"*
