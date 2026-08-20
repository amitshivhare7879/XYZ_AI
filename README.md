---
title: XYZ AI School ERP
emoji: 🎓
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# XYZ AI — Human-Like AI School Assistant Ecosystem

**XYZ AI** is an enterprise-grade Applied AI ecosystem designed as an intuitive, empathetic, and human-like assistant for **Students, Parents, Teachers, and School Leadership/Principals** across **Interactive Chat, Continuous Live Duplex Voice, and 60FPS 3D Canvas AI Avatars**.

Built on a clean monorepo architecture, XYZ AI enforces **deterministic application-layer RBAC security**, supports **11 Indian languages & Hinglish**, features a **3-state human escalation engine**, and provides **comprehensive School ERP operations** (Attendance, Academics, Timetables, Fee Invoices, Circulars, Homework, and Leave Management).

---

## 🌟 Key Highlights & Innovations

1. **4 Distinct AI Personas**:
   - **Student (Academic Assistant — Alex)**: Cheerful, motivating, Pomodoro study techniques, exam stress counseling, timetable & homework lookup.
   - **Parent (Parent Support Assistant — Maya)**: Empathetic, polite, child attendance tracking, grades inspection, fee payment, and leave application dispatch.
   - **Teacher (Teaching Assistant — Professor Orion)**: Professional, concise, voice/click attendance marking, class roster analysis, assignment submission audits.
   - **Principal (Executive Institutional Assistant — Athena)**: Strategic, analytical, school-wide attendance KPIs, fee collection analytics, faculty workload, and escalation resolution.
2. **Interactive 60FPS 3D Canvas Avatar & Viseme Lip-Sync**:
   - Real-time animated canvas avatar with expressive eye blinking, eyebrow articulation, ambient breathing, and realistic viseme mouth shaping synchronized to speech audio.
3. **Hands-Free Gemini Live Duplex Voice**:
   - Continuous two-way conversational voice with acoustic echo cancellation, automatic microphone squelching while the assistant speaks, and zero robotic interruptions.
4. **Natural Conversational Intelligence**:
   - Time-of-day and name-aware personalized greetings.
   - Multi-turn context memory retention across sessions.
   - Temporal query disambiguation (accurately distinguishes *yesterday* from *today*).
   - In-conversation corrections (*"No, I meant Science"*, *"Actually for next Monday"*).
   - Clarification questioning (*"What dates and reason should I list for your leave note?"*).
   - Empathetic counseling for academic anxiety.
5. **Real-Time Human Escalation State Machine**:
   - Interactive options: **“Talk to Teacher”** and **“Contact School Management”**.
   - Strict confirmation requirement before dispatching tickets.
   - Anti-hallucination honesty guarantee (never claims contact unless confirmed by the ERP service).
6. **Zero-Trust Application-Layer RBAC Security**:
   - JWT token authentication + verified entity ownership in code (never delegates authorization to LLM goodwill).
   - Immune to prompt injections, role-claim impersonation, and unauthorized child/financial access.
7. **100% Automated Test Coverage**: **50 / 50 comprehensive pytest unit & integration tests passing (100%)**.

---

## 📁 Repository Structure

```text
XYZ_AI/
├── 01_student_portal/         # Student Academic Assistant Portal (Avatar, Voice, Homework, Timetable)
│   ├── index.html             # Student dashboard frontend
│   └── package.json
├── 02_parent_portal/          # Parent Support Assistant Portal (Child Attendance, Fees, Reports)
│   ├── index.html             # Parent dashboard frontend
│   └── package.json
├── 03_staff_portal/           # Teacher / Staff Portal (Voice/Click Attendance, Rosters, Homework)
│   ├── index.html             # Teacher dashboard frontend
│   └── package.json
├── 04_management_portal/      # Principal / Leadership Portal (School KPIs, Fee Audits, Escalations)
│   ├── index.html             # Principal dashboard frontend
│   └── package.json
├── unified_login/             # Unified Single Sign-On Portal (Role Switching & Credentials)
│   └── index.html             # SSO login page
├── 05_xyz_ai/                 # FastAPI Backend & Multi-Agent Orchestration Core
│   ├── agent.py               # Human-like conversational orchestrator, memory & persona engine
│   ├── auth.py                # JWT authentication, demo credentials & role authorization
│   ├── erp_services.py        # Database-backed ERP business logic (Attendance, Fees, Grades, etc.)
│   ├── gemini_service.py      # Non-blocking Google Gemini integration with fast fallback
│   ├── groq_service.py        # Ultra-fast Groq Llama fallback engine with tool execution
│   ├── main.py                # FastAPI REST API, routing, static mounts & startup verification
│   ├── rbac.py                # Role-Based Access Control & parent-child ownership validator
│   ├── tools.py               # Safe ERP tool registry wrapping business services
│   ├── package.json
│   └── requirements.txt
├── shared/                    # Shared Schemas, Database Core & Multilingual Engine
│   ├── database.py            # Universal SQLite & PostgreSQL adapter (WAL mode, busy timeout)
│   ├── i18n.js                # Frontend vernacular UI dictionaries & dynamic script switcher
│   ├── multilingual_engine.py # Multi-lingual pattern translator & Indic TTS phoneme mapper
│   ├── schemas.py             # Pydantic data contracts for API requests, responses, and tokens
│   ├── seed_data.py           # Comprehensive Indian School ERP seed dataset (Grades 9-12 PCMB/Commerce)
│   └── types.ts               # TypeScript interface definitions
├── tests/                     # Automated Test Suite (50 Comprehensive Tests)
│   ├── conftest.py            # Isolated test database fixture
│   ├── test_erp_tools.py      # Student, Parent, Teacher, Principal ERP operations
│   ├── test_escalation.py     # 3-state escalation triggering, confirmation & mock dispatch
│   ├── test_fee_conversation_flow.py # Multi-turn fee context & persistent history
│   ├── test_human_assistant_personas.py # AI Personas, memory, corrections & empathy
│   ├── test_multilingual_intelligence.py # Hinglish, Hindi, Gujarati, Tamil, Marathi, Kannada
│   ├── test_rbac_security.py  # Prompt injection, fake role claims, and cross-parent access blocks
│   └── test_student_exam_and_subject_flow.py # Exam schedules & study tips
├── Dockerfile                 # Unified container deployment for Hugging Face Spaces / Cloud
├── app.py                     # Hugging Face Space entrypoint
├── .env.example               # Environment configuration template
└── README.md                  # Comprehensive Documentation
```

---

## 🎭 AI Personas & Role Matrix

| Persona | Portal Role | Voice & Tone | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **Alex** | **Student** | Friendly, motivating, enthusiastic | Homework assistance, exam schedules, study techniques (Pomodoro), timetable lookup, exam stress relief. |
| **Maya** | **Parent** | Empathetic, polite, clear, reassuring | Child attendance tracking, report card marks, fee balance inquiries & online UPI, leave note submissions. |
| **Professor Orion** | **Teacher** | Professional, collegial, efficient | Hands-free voice/click attendance marking, class roster analysis, homework submissions tracking. |
| **Athena** | **Principal** | Executive, analytical, data-driven | School-wide attendance KPIs, fee collection audits, class breakdown benchmarks, escalation ticket review. |

---

## 🛡️ Enterprise Security & RBAC Matrix

Security is strictly enforced in code at the **application layer** in [`05_xyz_ai/rbac.py`](file:///d:/Applied_AI/XYZ_AI/05_xyz_ai/rbac.py):

| Capability / Resource | Student | Parent | Teacher | Principal |
| :--- | :---: | :---: | :---: | :---: |
| **View Own Attendance** | ✅ | ❌ | ❌ | ❌ |
| **View Linked Child's Attendance** | ❌ | ✅ *(Own Child Only)* | ❌ | ❌ |
| **Mark Class Attendance** | ❌ | ❌ | ✅ *(Assigned Class)* | ✅ |
| **School-Wide Attendance KPIs** | ❌ | ❌ | ❌ | ✅ |
| **View Report Cards / Marks** | ✅ *(Self)* | ✅ *(Own Child)* | ✅ *(Assigned Class)* | ✅ *(All)* |
| **Fee Invoices & Online UPI** | ❌ | ✅ *(Own Child)* | ❌ | ✅ *(Aggregates)* |
| **Submit Leave Applications** | ✅ | ✅ | ❌ | ❌ |
| **Review / Manage Escalation Tickets** | ❌ | ❌ | ✅ | ✅ |

- **Parent-Child Link Isolation**: `validate_parent_student_ownership` ensures Parent A cannot inspect records for Parent B's child even if specifically requested by name or student ID.
- **Prompt Injection Defense**: Input guardrails detect and neutralize instructions attempting to override system rules, extract prompts, or elevate roles.

---

## 🗣️ Supported Languages & Multilingual Intelligence

XYZ AI dynamically processes conversations and outputs synthesized speech across **11 Indian languages + Hinglish**:

1. English (`en`)
2. Hinglish (`hinglish` — conversational Indian English + Hindi)
3. Hindi (`hi` — हिन्दी)
4. Gujarati (`gu` — ગુજરાતી)
5. Tamil (`ta` — தமிழ்)
6. Telugu (`te` — తెలుగు)
7. Marathi (`mr` — मराठी)
8. Bengali (`bn` — বাংলা)
9. Punjabi (`pa` — ਪੰਜਾਬੀ)
10. Kannada (`kn` — ಕನ್ನಡ)
11. Malayalam (`ml` — മലയാളം)
12. Urdu (`ur` — اردو)

---

## 🚀 Quickstart & Local Execution

### 1. Prerequisites
- Python 3.10+
- Modern Web Browser (Google Chrome or Microsoft Edge recommended for Web Speech & Web Audio APIs)

### 2. Setup Environment
```bash
# Clone the repository
git clone https://github.com/amitshivhare7879/XYZ_AI.git
cd XYZ_AI

# Install Python dependencies
pip install -r 05_xyz_ai/requirements.txt

# Seed the real-world School ERP database (Aug 2026 Academic Calendar)
python -m shared.seed_data
```

### 3. Launch the Server
```bash
# Start the unified FastAPI backend & portal server
uvicorn 05_xyz_ai.main:app --host 0.0.0.0 --port 7860 --reload
```

### 4. Access the Portals
Open your browser at `http://localhost:7860`:
- 🔐 **Unified Login**: [http://localhost:7860/login](http://localhost:7860/login)
- 🎓 **Student Portal**: [http://localhost:7860/student](http://localhost:7860/student)
- 👨‍👩‍👧 **Parent Portal**: [http://localhost:7860/parent](http://localhost:7860/parent)
- 👩‍🏫 **Staff / Teacher Portal**: [http://localhost:7860/staff](http://localhost:7860/staff)
- 🏛️ **Management / Principal Portal**: [http://localhost:7860/management](http://localhost:7860/management)
- 📚 **Swagger API Documentation**: [http://localhost:7860/docs](http://localhost:7860/docs)

---

## 🔑 Demo Login Accounts

| Role | Email | Password | Pre-Assigned Context |
| :--- | :--- | :--- | :--- |
| **Student** | `rahul.patel@student.school.edu` | `password123` | Rahul Patel (Grade 10-A, Roll #10A-01) |
| **Parent** | `amit.patel@gmail.com` | `password123` | Mr. Amit Patel (Father of Rahul Patel) |
| **Teacher** | `anjali.verma@school.edu` | `password123` | Mrs. Anjali Verma (Class Teacher, Grade 10-A) |
| **Principal** | `principal@school.edu` | `password123` | Dr. Rajesh Sharma (School Leadership / Principal) |

---

## 🧪 Automated Testing Suite

The project includes **50 automated pytest unit and integration tests** passing with 100% success rate:

```bash
# Run the complete test suite
pytest tests/ -v
```

### Verified Test Breakdown (50 / 50 Passing):
- **12 ERP Tool Execution Tests**: Student, Parent, Teacher, and Principal ERP operations.
- **4 Human Escalation Tests**: 3-state state machine, user confirmation, and honest mock dispatch.
- **10 Human Persona & Empathy Tests**: Memory retention, follow-ups, in-conversation corrections, and exam stress relief.
- **12 Multilingual Intelligence Tests**: Vernacular translation and tool accuracy across Hindi, Gujarati, Tamil, Marathi, Kannada, and Hinglish.
- **9 RBAC Security & Guardrail Tests**: Parent-child link isolation, unauthorized fee blocks, fake role claims, and prompt injection defense.
- **2 Student Exam & Subject Guidance Tests**: Timetables, exam schedules, and Pomodoro study technique advice.
- **1 Fee Conversation Flow Test**: Multi-turn invoice and payment history persistence.

---

## 📦 Package for Submission / Distribution

To create a clean submission ZIP archive without cache directories, run:
```bash
python make_submission_zip.py
```
This produces `XYZ_AI_Submission.zip` in the root directory.

---

## 📄 License
This project is built for the **XYZ AI Applied AI Competition / Deployment**. All rights reserved.
