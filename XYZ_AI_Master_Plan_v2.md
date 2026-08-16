# XYZ AI — Master Implementation Plan (v2)
Human-Like AI School ERP Assistant — final scope & architecture, reconciled with the Antigravity plan

Decisions locked this round: **full ERP scope** (not attendance-only) and **Supabase Postgres + Row Level Security** as the database.

---

## 1. Scope — full ERP capability matrix

| Domain | Student | Parent | Teacher | Principal / Management |
|---|---|---|---|---|
| Attendance | View own stats, recent dates | View child's attendance & absence trends | Mark daily attendance, view class roster | School-wide rate, low-attendance flags, class comparison |
| Grades & academics | View grades, upcoming tests, homework | View child's report card, alerts, strengths/weaknesses | Enter/update grades, list low-performing students | Department/grade-level distributions, pass/fail metrics |
| Fees & billing | **No access** | Check balance, due dates, payment history/receipts | **No access** | Collection overview, arrears, defaulters report |
| Timetable & events | Next class, daily timetable, exam schedule | School calendar, holidays, PTM dates | Teaching schedule, free periods, substitution duties | Faculty allocation, room bookings, event calendar |
| Leave & notices | Submit leave notes, view circulars | Submit absence notice for child, view announcements | Approve student leave, broadcast class notice | Post school-wide notices, view staff/student leave quotas |
| Escalation | Request counselor/academic advisor | Request callback from teacher or management | Request admin support/principal meeting | Review escalation queue, dispatch & resolve tickets |

This is a real expansion beyond the brief's four attendance-only use cases — going in with eyes open, that's the tradeoff you accepted for a more complete demo.

---

## 2. Repository structure — monorepo (corrected)

```
XYZ_AI/                        ← single GitHub repository
├── 01_student_portal/         (Next.js + Tailwind)
├── 02_parent_portal/          (Next.js + Tailwind — multi-child switcher)
├── 03_staff_portal/           (Next.js + Tailwind — roster, quick attendance marker)
├── 04_management_portal/      (Next.js + Tailwind — analytics, escalation monitor)
├── 05_xyz_ai/                 (FastAPI — orchestrator, RBAC, tools, STT/TTS, mock ERP APIs)
└── shared/                    (shared TS + Pydantic schema definitions, seed data)
```

Correction from the previous plan: I'd originally recommended 5 fully independent GitHub repos. Re-reading the brief, the "Repository Structure" section is drawn as a nested folder tree, and Submission asks for **"GitHub Repository"** — singular. One monorepo with five clearly separated folders is the more literal, safer reading, and it's what's reflected here.

**Thin-client rule stays**: the four portals have no direct DB access and no LLM keys. Every action routes through `05_xyz_ai` with the user's JWT.

---

## 3. Tech stack

| Layer | Choice |
|---|---|
| Core AI engine | FastAPI + LangChain + Gemini API |
| RBAC / tool layer | Plain Python, deterministic — not LLM-decided |
| Auth | Supabase Auth (JWT, role as a custom claim) |
| Database | **Supabase Postgres + Row Level Security** (confirmed) |
| Frontends | Next.js + TypeScript + Tailwind (×4 portals) |
| STT | Web Speech API (zero latency) + Whisper (accuracy fallback, Indian accents) |
| TTS | HeadTTS (Kokoro) — free, outputs audio + viseme timestamps |
| Avatar | Ready Player Me (GLB model, ARKit blendshapes) + wawa-lipsync/TalkingHead.js via React Three Fiber |
| Escalation | Own FastAPI route + Supabase table, modeled as an unreliable external system |

---

## 4. System architecture

```
[ Chat ]  [ Voice: STT/TTS ]  [ AI Avatar ]        ← 4 portals, per role
        \        |        /
         v       v       v
      ┌─────────────────────────────┐
      │   xyz-ai core engine         │  role detection, intent, context,
      │                              │  persona selection, language
      └──────────────┬──────────────┘
                      v
      ┌─────────────────────────────┐
      │   RBAC / tool layer          │  validates role + entity ownership
      │   (application code)         │  before ANY read or write
      └──────────────┬──────────────┘
                      v
      ┌───────────────────────────────────────────────────┐
      │              Tool execution gateway                 │
      │  Attendance │ Academics │ Fees │ Timetable │ Notices │
      │  Leave │ Escalation                                  │
      └──────────────────────┬──────────────────────────────┘
                              v
      ┌─────────────────────────────────────┐
      │  Supabase (Postgres + RLS)            │
      └─────────────────────────────────────┘
```

---

## 5. Data model (expanded for full ERP)

| Table | Key fields | Ownership check used by RLS |
|---|---|---|
| `users` | id, auth_id, role, name, preferred_language | — |
| `students` | id, name, class_id | — |
| `classes` | id, name, teacher_id | — |
| `parent_student_links` | parent_user_id, student_id | parent → student |
| `teacher_class_links` | teacher_user_id, class_id | teacher → class |
| `attendance` | student_id, date, status, marked_by | via student → parent/teacher link |
| `subjects` / `exams` / `grades` | student_id, subject_id, exam_id, score | via student → parent/teacher link |
| `homework` | class_id, subject_id, due_date, description | via class → teacher link |
| `fee_invoices` | student_id, term, amount, due_date, status | via student → parent link |
| `fee_payments` | invoice_id, amount, paid_at, receipt_no | via invoice → student → parent link |
| `timetable_slots` | class_id, day, period, subject_id, teacher_id | via class link |
| `events` | title, date, type (PTM/holiday/exam), audience_role | broad read, role-filtered |
| `notices` | id, posted_by, audience_role, body, created_at | role-filtered read |
| `leave_applications` | student_id or staff_id, dates, reason, status, approved_by | via student/staff link |
| `escalation_tickets` | id, requested_by, role, target, status (pending/confirmed/failed), created_at | requester-scoped |
| `conversation_sessions` / `conversation_messages` | user_id, session_id, content | user-scoped |
| `audit_log` | actor_id, action, entity, timestamp | append-only, staff/mgmt read |

Every table with a student/staff owner gets an RLS policy scoping `SELECT`/`UPDATE` to rows the requesting `auth.uid()` is actually linked to — this is enforced whether or not the app-layer check is also correct.

---

## 6. Auth & RBAC — request flow

1. Portal sends the request to `xyz-ai` with the Supabase JWT.
2. `xyz-ai` verifies the JWT signature server-side; role + user_id come from the **verified token only**, never from request body or chat text.
3. Gemini proposes a structured tool call (e.g. `get_student_grades(student_name="Rahul")`).
4. Tool layer checks the permission matrix (§1, formalized as role × domain → allow/deny).
5. Tool layer checks entity ownership (e.g. does this parent's `parent_student_links` row actually include "Rahul"?).
6. **Both pass** → query runs, Gemini turns the result into a natural, persona-toned response.
   **Either fails** → tool layer returns a structured "unauthorized" error; Gemini refuses politely, no partial data leaks, no explanation of *why* the check exists beyond "I can't help with that."
7. Every read is checked; every write (mark attendance, enter grade, approve leave, post notice) is checked the same way *and* logged to `audit_log`.

---

## 7. Persona & conversation behavior (unchanged from v1)

Pipeline: auth resolve → persona select (Student: friendly/supportive; Parent: caring/patient; Teacher: professional; Principal: professional/executive) → context load → intent+entity extraction → RBAC check → tool call → persona-toned, correctly-languaged response.

Human-like behaviors: session-start greeting, mid-conversation correction handling ("no, I meant Rahul" → re-confirm, don't guess), clarification when a required entity is missing or ambiguous (never call a tool on a guess).

---

## 8. Language support (unchanged)

Detected from first message or set via toggle, stored per user, reused across sessions. Intent/RBAC always run on a normalized English representation internally; only generation and TTS are language-specific. Covers all 11 required languages. Known risk carried over: TTS voice coverage is thinner for Punjabi/Urdu on free neural TTS — flag in the README rather than discover it live.

---

## 9. Voice + avatar pipeline (unchanged)

`Voice → STT (Web Speech/Whisper) → xyz-ai text pipeline → TTS (HeadTTS/Kokoro, audio + viseme timestamps) → Avatar (Ready Player Me + wawa-lipsync blendshapes)`. Fully free, client-side/self-hosted, no GPU server dependency.

---

## 10. Escalation — per role, still honest about failure

Each role's escalation target differs (student → counselor, parent → class teacher/management, teacher → admin/principal, principal → reviews the queue itself), but the state machine is identical for all of them:

1. Bot detects dissatisfaction or an explicit request for a human → presents explicit options (never auto-triggers).
2. User confirms → ticket created as `pending`, mock service called async with a timeout.
3. **Success** → `confirmed`, bot states this plainly.
   **Timeout/error** → `failed`, logged for manual follow-up, bot offers retry or a direct fallback contact — never claims success without a real confirmation object back.
4. Management portal gets a live queue view of all tickets (pending/confirmed/failed) across the school, per the capability matrix.

---

## 11. Security — 6-point mapping (updated for the full module set)

| Threat | Mechanism | Enforced where |
|---|---|---|
| Prompt injection | LLM only emits structured/typed tool calls; tool results are data, never re-interpreted as instructions | `xyz-ai` tool layer |
| Unauthorized data access | RBAC + ownership join on every module (attendance, grades, fees, timetable, leave, notices) | App layer + Supabase RLS, independently |
| System-prompt extraction | Personas refuse meta-questions about their own instructions; nothing sensitive lives in the prompt to begin with | Prompt design + output filtering |
| API-key/credential extraction | Secrets exist only in server env vars, never interpolated into anything sent to Gemini | `xyz-ai`, outside the LLM entirely |
| Fake role claims | Role comes only from the verified JWT; "I'm the principal" in chat text has zero effect | `xyz-ai`, before intent runs |
| Unauthorized actions | Every mutation (mark attendance, enter grade, approve leave, post notice) checked and logged | App layer, `audit_log` |

Automated coverage: `pytest tests/test_rbac_security.py` — fake roles, cross-parent child access, student mutation attempts, prompt injection attempts, one test per threat above.

---

## 12. Database sizing — reconfirmed with the expanded scope

Even with grades, fees, timetable, leave, and notices added, mock data at assessment scale (~50 students, 10 teachers, 40 parents, a school year of records) stays well under Supabase's free-tier 500 MB. The two real free-tier risks are unchanged: auto-pause after 7 days idle (mitigate with a scheduled ping if needed) and no automated backups (do a manual export before the final demo). No reason to revisit this with the larger scope.

---

## 13. Testing plan

- `pytest tests/test_rbac_security.py` — all 6 threat vectors
- `pytest tests/test_erp_tools.py` — attendance, grades, fees, timetable, leave, escalation ticket creation
- `pytest tests/test_escalation.py` — confirms the bot never reports "confirmed" without a real mock-service response
- Manual: live chat in each of the 4 portals (role-specific tone + access boundaries), live voice + avatar lip-sync check, language switching across at least 4–5 of the 11 languages for the demo

---

## 14. Submission checklist

- [ ] One GitHub repository containing all five folders
- [ ] Complete source code
- [ ] Root README (system overview) + per-folder README, including honest notes on avatar fidelity and TTS language-coverage gaps
- [ ] Working chat interface (non-negotiable minimum bar)
- [ ] Short demo video or live demonstration

---

## 15. Build order

1. Supabase schema + RLS policies for **all** tables in §5 — everything depends on this.
2. `xyz-ai` core: JWT auth → RBAC/tool layer → mock APIs, starting with Attendance, then Academics, Fees, Timetable, Notices, Leave, Escalation. Test each module with raw HTTP calls before wiring the LLM.
3. Intent + persona layer on top (Gemini emitting structured tool calls).
4. One portal end-to-end (`parent_portal` — richest RBAC surface: attendance + grades + fees + escalation, all ownership-checked).
5. Escalation service, all four role targets.
6. Remaining three portals.
7. Language support (detection, storage, localized generation).
8. Voice + avatar wiring.
9. Full `pytest` suite (§13) + a deliberate attempt to break your own RBAC before calling it done.

---

## 16. Full coverage check

| Source requirement | Covered by |
|---|---|
| Brief: attendance use cases (all 4 roles) | §1 row 1, §5, §6 |
| Brief: chat/voice/avatar, human-like behavior | §7, §9 |
| Brief: escalation, no false confirmation | §10 |
| Brief: 11 languages | §8 |
| Brief: repository structure | §2 (corrected to monorepo) |
| Brief: all 6 security points | §11 |
| Brief: submission requirements | §14 |
| Antigravity addition: full ERP modules | §1, §5, §6 |
| Antigravity addition: RBAC sequence flow | §6 |
| Antigravity addition: test suite structure | §13 |
