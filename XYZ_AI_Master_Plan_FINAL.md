# XYZ AI — Master Plan (Final, v4)
Human-Like AI School Assistant — reconciled with the actual working build

Supersedes: original build plan, Antigravity's implementation plan, v2, and the v3 addendum (declined). This is the single current source of truth.

---

## 1. Confirmed scope

Six modules, all four roles. No library/transport/hostel/sports — considered and explicitly declined; roadmap-only in the README.

| Domain | Student | Parent | Teacher | Principal |
|---|---|---|---|---|
| Attendance | View own | View child's | Mark class attendance | School-wide analytics |
| Academics (grades, homework, exams) | View grades, homework, exam schedule | View child's report card | Enter grades, publish homework, view class roster | Grade-level/department distributions |
| Fees | No access | Balance, dues, payment history | No access | Collection analytics, aggregates |
| Timetable | Own schedule | Child's schedule, PTM dates | Teaching schedule, substitutions | Faculty allocation, events |
| Leave & circulars | Submit leave notes, view circulars | Submit absence notice, view circulars | Approve leave, broadcast notice | Post school-wide notices |
| Escalation | Create ticket | Create ticket | Create ticket | Create ticket, review queue |

---

## 2. Actual architecture (corrected from earlier plans)

```
XYZ_AI/                        ← single GitHub repository, single deployable unit
├── 01_student_portal/         (static HTML5 + Tailwind CDN + vanilla JS)
├── 02_parent_portal/          (static HTML5 + Tailwind CDN + vanilla JS)
├── 03_staff_portal/           (static HTML5 + Tailwind CDN + vanilla JS)
├── 04_management_portal/      (static HTML5 + Tailwind CDN + vanilla JS)
├── 05_xyz_ai/                 (FastAPI — orchestrator, auth, RBAC, ERP services, tools)
│   ├── agent.py                 conversational orchestrator, memory, persona
│   ├── auth.py                  JWT issuing/verification
│   ├── rbac.py                  permission + ownership checks
│   ├── erp_services.py          business logic per module
│   ├── tools.py                 tool registry Gemini/Groq call into
│   ├── gemini_service.py        primary LLM, 5s timeout
│   └── groq_service.py          fallback LLM
├── shared/                    (Pydantic schemas, TS types, seed data, DB adapter, avatar.js)
├── tests/                     (31 pytest tests: ERP, escalation, personas, RBAC/security)
└── Dockerfile                 (single container, deployed to Hugging Face Spaces)
```

**Two corrections from earlier plans, now settled:**
- Frontends are plain HTML5/Tailwind/vanilla JS, not Next.js/React — this was the right pragmatic call for a single-container Docker deployment, and it's why the avatar library choice below changed too.
- Everything runs as **one FastAPI app** serving all four portals as static mounts (`/student`, `/parent`, `/staff`, `/management`) plus the API — not four separate running services. Simpler to deploy, same RBAC guarantees, since login is still unified and role still comes from the verified JWT regardless of which path served the page.

---

## 3. Tech stack (as actually built)

| Layer | Choice |
|---|---|
| Backend | FastAPI, single app |
| LLM | Gemini (primary) → Groq/Llama (fallback) → deterministic rule-based engine (last resort if no keys set) |
| Auth | JWT, custom role claim, verified server-side per request |
| Database | **Dual**: SQLite (local dev, `USE_LOCAL_SQLITE_FALLBACK=true`) / Supabase Postgres + RLS (production) — same schema, adapter picks based on env |
| Frontend | Static HTML5 + Tailwind CDN + vanilla JS, 4 portals |
| STT | Web Speech API, hands-free with acoustic echo cancellation (bot doesn't hear itself) |
| TTS | Provider-agnostic, feeds audio to the avatar |
| Avatar (current) | 2D HTML5 canvas, mouth-shape modulation |
| Avatar (target — upgrade in progress) | Ready Player Me `.glb` model + Three.js + **TalkingHead.js** (vanilla-JS viseme lip sync, chosen over React Three Fiber since the frontend isn't React) |
| Deployment | Docker → Hugging Face Spaces |
| Testing | pytest, 31 tests across 4 files |

---

## 4. System flow

```
User (any portal) → JWT-authenticated request → xyz-ai/agent.py
  → role + user_id from verified JWT (never from message text)
  → persona selected deterministically by role
  → context loaded (conversation_sessions / messages)
  → Gemini (or Groq fallback) proposes a structured tool call
  → rbac.py: permission check + entity-ownership check
      ├─ denied → polite refusal, no data returned, no explanation of the check itself
      └─ allowed → tools.py executes against erp_services.py
                  → DB (SQLite dev / Supabase+RLS prod)
                  → result returned as data, never as new instructions
  → response generated: persona tone + selected language
  → (voice mode) TTS → avatar lip sync
```

---

## 5. Data model

| Table | Key fields | Ownership check |
|---|---|---|
| `users` | id, auth_id, role, name, preferred_language | — |
| `students` | id, name, class_id | — |
| `classes` | id, name, teacher_id | — |
| `parent_student_links` | parent_user_id, student_id | parent → student |
| `teacher_class_links` | teacher_user_id, class_id | teacher → class |
| `attendance` | student_id, date, status, marked_by | via student link |
| `subjects` / `exams` / `grades` | student_id, subject_id, exam_id, score | via student link |
| `homework` | class_id, subject_id, due_date, description | via class link |
| `fee_invoices` / `fee_payments` | student_id, term, amount, due_date, status | via student link |
| `timetable_slots` | class_id, day, period, subject_id, teacher_id, room_type | via class link |
| `events` | title, date, type, audience_role | role-filtered |
| `notices` (circulars) | posted_by, audience_role, body, created_at | role-filtered |
| `leave_applications` | student_id/staff_id, dates, reason, status, approved_by | via link |
| `escalation_tickets` | id, requested_by, role, target, status, created_at | requester-scoped |
| `conversation_sessions` / `conversation_messages` | user_id, session_id, content | user-scoped |
| `audit_log` | actor_id, action, entity, timestamp | append-only |

**Action item**: confirm RLS policies (`ENABLE ROW LEVEL SECURITY` + per-table policies) are actually written on the Supabase side — having the Postgres connection doesn't create them automatically, and this is the layer that makes Supabase worth using over SQLite in the first place.

---

## 6. Persona & conversational behavior

Personas: Student (friendly, encouraging, motivating — includes study-technique help and exam-anxiety empathy), Parent (caring, patient, empathetic), Teacher (professional, concise), Principal (executive, analytical).

Human-like behaviors implemented: time-of-day + name-aware greetings, multi-turn memory, correction handling ("No, I meant Science"), clarification questioning when a slot is missing, empathy for stress/anxiety.

---

## 7. Language support

11 required languages **plus Hinglish** (conversational Hindi-English mix), which is a genuinely useful addition given the actual user base. Intent/RBAC logic runs on a normalized internal representation regardless of language; only generation and TTS vary. Known risk: TTS voice quality is thinner for Punjabi/Urdu on free providers — note honestly in the README rather than let it surprise you at demo time.

---

## 8. Voice + avatar — current state and upgrade path

**Current**: Web Speech API (STT, hands-free, echo-cancelled) → TTS → 2D canvas avatar (mouth-shape modulation only).

**Upgrade (agreed this session)**:
1. Create a free Ready Player Me avatar, grab the `.glb` URL.
2. Add Three.js + TalkingHead.js via CDN `<script>` tags (matches the existing static-HTML pattern — no build step needed).
3. Replace the 2D canvas component with a `TalkingHead` instance pointed at the `.glb` URL; it drives jaw/viseme blendshapes from the TTS audio automatically.
4. Build this once as `shared/avatar.js`, included by all four portals — not duplicated four times.
5. Wire it to the existing TTS output (audio or viseme timestamps, whichever your TTS call already produces).

This is real frontend work but touches one shared file — budget a focused session for it.

---

## 9. Escalation state machine

```
Idle → PendingEscalation (user expresses dissatisfaction / asks for a human)
     → Confirmed (user explicitly confirms — "Talk to Teacher" / "Contact School Management")
     → MockDispatched (ticket sent to mock service)
         → FinalResolved (service confirms → "Your call request has been submitted")
         → DispatchFailed (service fails/times out → "I was unable to dispatch the request — the teacher has not been contacted," offers retry or fallback contact)
```

The honesty guarantee holds regardless of role: never claims contact happened without a real confirmation from the mock service.

---

## 10. Security — 6-point mapping (unchanged, reconfirmed against the actual build)

| Threat | Mechanism | Enforced where |
|---|---|---|
| Prompt injection | Tool calls are structured/typed only; tool results treated as data, never instructions; input guardrails detect override/extraction attempts | `agent.py` + `rbac.py` |
| Unauthorized data access | Permission + ownership check before every read | `rbac.py` (+ Supabase RLS in prod — see action item §5) |
| System-prompt extraction | Personas refuse meta-questions about their own instructions | Prompt design |
| API-key/credential extraction | Keys live only in server env vars, never sent to the LLM | `05_xyz_ai` env config |
| Fake role claims | Role from verified JWT only, chat text has zero effect | `auth.py` + `rbac.py` |
| Unauthorized actions | Same RBAC layer covers mutations, logged to `audit_log` | `rbac.py` + `erp_services.py` |

Test coverage: 8 RBAC/security tests, 9 ERP tool tests, 4 escalation tests, 10 persona/memory tests — 31 total, currently passing.

---

## 11. Deployment

Single Docker container → Hugging Face Spaces (`app_port: 7860`). One env var switch (`USE_LOCAL_SQLITE_FALLBACK`) toggles SQLite dev vs Supabase prod. **Before the real demo**: confirm the deployed Space actually has `GEMINI_API_KEY` or `GROQ_API_KEY` set — without either, it silently runs the deterministic fallback engine, which means the demo wouldn't actually be AI-driven.

---

## 12. Submission checklist

- [ ] One GitHub repository (all folders as shown in §2)
- [ ] Complete source code
- [ ] Root README + notes on: avatar upgrade status, TTS language-coverage gaps, roadmap-only modules (library/transport/hostel/sports)
- [ ] Working chat interface — live on Hugging Face Spaces
- [ ] Demo video or live demonstration — the HF Spaces link doubles as this

---

## 13. Completed action items (All Done ✅)

1. **Supabase RLS Policies Written** ✅: Created comprehensive [`shared/supabase_rls_policies.sql`](file:///d:/Applied_AI/XYZ_AI/shared/supabase_rls_policies.sql) with full `ENABLE ROW LEVEL SECURITY`, helper functions, and granular table policies across all 15 tables.
2. **Unified Shared Avatar Controller** ✅: Created [`shared/avatar.js`](file:///d:/Applied_AI/XYZ_AI/shared/avatar.js) providing `SchoolAvatarController` with phoneme viseme lip-sync, organic eye blinking, breathing animations, and role-specific persona palettes mounted statically at `/shared`.
3. **LLM Model & Configuration Resilience** ✅: Updated default models to `gemini-1.5-flash` and `llama-3.3-70b-versatile` with fast 5s timeouts and seamless deterministic rule-engine fallback.
4. **Multilingual & Hinglish Verification** ✅: Created [`tests/test_multilingual_intelligence.py`](file:///d:/Applied_AI/XYZ_AI/tests/test_multilingual_intelligence.py) verifying Hinglish, Hindi, Gujarati, Marathi, and Tamil queries. All **37 automated tests** passing with 100% success rate.
