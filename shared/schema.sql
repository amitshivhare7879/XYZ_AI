-- ==============================================================================
-- XYZ AI — School ERP Ecosystem Database Schema
-- Compatible with Supabase Postgres & Row Level Security (RLS)
-- ==============================================================================

-- Enable UUID extension if not enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table (Core identity, synced with Supabase Auth auth.users)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    auth_id UUID UNIQUE, -- References auth.users(id) in Supabase
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('student', 'parent', 'teacher', 'principal')),
    phone VARCHAR(20),
    preferred_language VARCHAR(20) DEFAULT 'en',
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Classes Table
CREATE TABLE IF NOT EXISTS classes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL, -- e.g. "Grade 10-A"
    grade INT NOT NULL,       -- e.g. 10
    section VARCHAR(10) NOT NULL, -- e.g. "A"
    class_teacher_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Students Table
CREATE TABLE IF NOT EXISTS students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(id), -- For student portal login
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    class_id UUID REFERENCES classes(id),
    date_of_birth DATE,
    gender VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Parent-Student Links (RBAC Entity Ownership for Parents)
CREATE TABLE IF NOT EXISTS parent_student_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_user_id UUID NOT NULL REFERENCES users(id),
    student_id UUID NOT NULL REFERENCES students(id),
    relationship VARCHAR(50) DEFAULT 'Parent', -- 'Father', 'Mother', 'Guardian'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(parent_user_id, student_id)
);

-- 5. Subjects Table
CREATE TABLE IF NOT EXISTS subjects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL, -- e.g. 'Mathematics', 'Science', 'English'
    code VARCHAR(20) UNIQUE NOT NULL
);

-- 6. Teacher-Class Links (RBAC Entity Ownership for Teachers)
CREATE TABLE IF NOT EXISTS teacher_class_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    teacher_user_id UUID NOT NULL REFERENCES users(id),
    class_id UUID NOT NULL REFERENCES classes(id),
    subject_id UUID REFERENCES subjects(id),
    is_class_teacher BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(teacher_user_id, class_id, subject_id)
);

-- 7. Daily Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id),
    class_id UUID NOT NULL REFERENCES classes(id),
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'absent', 'late', 'excused')),
    marked_by UUID REFERENCES users(id),
    remarks TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, date)
);

-- 8. Exams Table
CREATE TABLE IF NOT EXISTS exams (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL, -- e.g. 'Mid-Term Examination 2026'
    term VARCHAR(50) NOT NULL,   -- e.g. 'Term 1'
    academic_year VARCHAR(20) NOT NULL, -- e.g. '2025-2026'
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. Grades / Marks Table
CREATE TABLE IF NOT EXISTS grades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id),
    subject_id UUID NOT NULL REFERENCES subjects(id),
    exam_id UUID NOT NULL REFERENCES exams(id),
    marks_obtained NUMERIC(5, 2) NOT NULL,
    max_marks NUMERIC(5, 2) NOT NULL DEFAULT 100.00,
    grade VARCHAR(5), -- 'A+', 'A', 'B', etc.
    remarks TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, subject_id, exam_id)
);

-- 10. Homework Table
CREATE TABLE IF NOT EXISTS homework (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    class_id UUID NOT NULL REFERENCES classes(id),
    subject_id UUID NOT NULL REFERENCES subjects(id),
    teacher_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    assigned_date DATE NOT NULL,
    due_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. Fee Invoices Table
CREATE TABLE IF NOT EXISTS fee_invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id),
    term VARCHAR(50) NOT NULL, -- e.g. 'Term 1 (Apr - Jul 2026)'
    academic_year VARCHAR(20) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('paid', 'partial', 'unpaid', 'overdue')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 12. Fee Payments Table
CREATE TABLE IF NOT EXISTS fee_payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID NOT NULL REFERENCES fee_invoices(id),
    amount_paid NUMERIC(10, 2) NOT NULL,
    payment_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50) DEFAULT 'Online UPI',
    receipt_no VARCHAR(100) UNIQUE NOT NULL,
    transaction_ref VARCHAR(100)
);

-- 13. Timetable Slots Table
CREATE TABLE IF NOT EXISTS timetable_slots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    class_id UUID NOT NULL REFERENCES classes(id),
    day_of_week VARCHAR(20) NOT NULL CHECK (day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')),
    period_number INT NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    subject_id UUID NOT NULL REFERENCES subjects(id),
    teacher_id UUID NOT NULL REFERENCES users(id),
    room_number VARCHAR(50)
);

-- 14. School Events & Calendar Table
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('ptm', 'holiday', 'exam', 'cultural', 'sports', 'general')),
    target_role VARCHAR(50) DEFAULT 'all'
);

-- 15. School Notices / Announcements Table
CREATE TABLE IF NOT EXISTS notices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    posted_by UUID REFERENCES users(id),
    target_role VARCHAR(50) DEFAULT 'all' CHECK (target_role IN ('all', 'student', 'parent', 'teacher', 'principal')),
    is_urgent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 16. Leave Applications Table
CREATE TABLE IF NOT EXISTS leave_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    applicant_user_id UUID NOT NULL REFERENCES users(id),
    applicant_role VARCHAR(50) NOT NULL,
    student_id UUID REFERENCES students(id), -- If submitted by a parent or student
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    approved_by UUID REFERENCES users(id),
    remarks TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 17. Escalation Tickets Table (3-state reliable escalation)
CREATE TABLE IF NOT EXISTS escalation_tickets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    requested_by_user_id UUID NOT NULL REFERENCES users(id),
    requested_by_role VARCHAR(50) NOT NULL,
    student_id UUID REFERENCES students(id),
    target_entity VARCHAR(50) NOT NULL CHECK (target_entity IN ('teacher', 'management', 'principal', 'counselor')),
    target_user_id UUID REFERENCES users(id),
    reason TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'failed', 'resolved')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT
);

-- 18. Conversational Sessions & Memory
CREATE TABLE IF NOT EXISTS conversation_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    session_token VARCHAR(255) UNIQUE NOT NULL,
    language VARCHAR(20) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversation_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES conversation_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system', 'tool')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 19. Security & Operations Audit Log
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor_user_id UUID REFERENCES users(id),
    actor_role VARCHAR(50),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id VARCHAR(100),
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ==============================================================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE parent_student_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE teacher_class_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE grades ENABLE ROW LEVEL SECURITY;
ALTER TABLE fee_invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE fee_payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE timetable_slots ENABLE ROW LEVEL SECURITY;
ALTER TABLE notices ENABLE ROW LEVEL SECURITY;
ALTER TABLE leave_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE escalation_tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- Sample Policies (Supabase auth.uid() mapped to users.auth_id)
-- 1. Users can read own user record
DROP POLICY IF EXISTS user_read_own ON users;
CREATE POLICY user_read_own ON users
    FOR SELECT USING (auth_id = auth.uid() OR auth.jwt() ->> 'role' = 'principal');

-- 2. Parents can only see attendance of their linked children
DROP POLICY IF EXISTS parent_read_child_attendance ON attendance;
CREATE POLICY parent_read_child_attendance ON attendance
    FOR SELECT USING (
        auth.jwt() ->> 'role' = 'principal'
        OR auth.jwt() ->> 'role' = 'teacher'
        OR student_id IN (
            SELECT psl.student_id FROM parent_student_links psl
            JOIN users u ON u.id = psl.parent_user_id
            WHERE u.auth_id = auth.uid()
        )
        OR student_id IN (
            SELECT s.id FROM students s
            JOIN users u ON u.id = s.user_id
            WHERE u.auth_id = auth.uid()
        )
    );

-- 3. Teachers can mark attendance for classes they are assigned to
DROP POLICY IF EXISTS teacher_mark_attendance ON attendance;
CREATE POLICY teacher_mark_attendance ON attendance
    FOR INSERT WITH CHECK (
        auth.jwt() ->> 'role' = 'principal'
        OR class_id IN (
            SELECT tcl.class_id FROM teacher_class_links tcl
            JOIN users u ON u.id = tcl.teacher_user_id
            WHERE u.auth_id = auth.uid()
        )
    );

-- 4. Fee Invoices visible only to parent of student or Principal
DROP POLICY IF EXISTS parent_read_fee_invoices ON fee_invoices;
CREATE POLICY parent_read_fee_invoices ON fee_invoices
    FOR SELECT USING (
        auth.jwt() ->> 'role' = 'principal'
        OR student_id IN (
            SELECT psl.student_id FROM parent_student_links psl
            JOIN users u ON u.id = psl.parent_user_id
            WHERE u.auth_id = auth.uid()
        )
    );
