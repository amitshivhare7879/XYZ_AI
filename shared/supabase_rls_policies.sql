-- ==============================================================================
-- XYZ AI — Supabase PostgreSQL Row-Level Security (RLS) Policy Definitions
-- Complete RLS policies for production deployment with Supabase Auth
-- ==============================================================================

-- Enable RLS across all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE parent_student_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE teacher_class_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE exams ENABLE ROW LEVEL SECURITY;
ALTER TABLE grades ENABLE ROW LEVEL SECURITY;
ALTER TABLE fee_invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE fee_payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE timetable_slots ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE notices ENABLE ROW LEVEL SECURITY;
ALTER TABLE homework ENABLE ROW LEVEL SECURITY;
ALTER TABLE leave_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE escalation_tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- Helper function: Get Current User's ID from users table matching auth.uid()
CREATE OR REPLACE FUNCTION current_app_user_id() 
RETURNS UUID AS $$
    SELECT id FROM users WHERE auth_id = auth.uid() LIMIT 1;
$$ LANGUAGE sql STABLE SECURITY DEFINER;

-- Helper function: Get Current User's Role
CREATE OR REPLACE FUNCTION current_app_user_role() 
RETURNS VARCHAR AS $$
    SELECT COALESCE(auth.jwt() ->> 'role', (SELECT role FROM users WHERE auth_id = auth.uid() LIMIT 1));
$$ LANGUAGE sql STABLE SECURITY DEFINER;

-- ------------------------------------------------------------------------------
-- 1. Users Table
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS users_select_policy ON users;
CREATE POLICY users_select_policy ON users
    FOR SELECT USING (
        auth_id = auth.uid() 
        OR current_app_user_role() IN ('principal', 'teacher')
    );

DROP POLICY IF EXISTS users_update_policy ON users;
CREATE POLICY users_update_policy ON users
    FOR UPDATE USING (auth_id = auth.uid())
    WITH CHECK (auth_id = auth.uid());

-- ------------------------------------------------------------------------------
-- 2. Classes & Subjects
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS classes_select_all ON classes;
CREATE POLICY classes_select_all ON classes FOR SELECT USING (true);

DROP POLICY IF EXISTS subjects_select_all ON subjects;
CREATE POLICY subjects_select_all ON subjects FOR SELECT USING (true);

-- ------------------------------------------------------------------------------
-- 3. Students Table
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS students_select_policy ON students;
CREATE POLICY students_select_policy ON students
    FOR SELECT USING (
        current_app_user_role() IN ('principal', 'teacher')
        OR user_id = current_app_user_id()
        OR id IN (
            SELECT student_id FROM parent_student_links 
            WHERE parent_user_id = current_app_user_id()
        )
    );

-- ------------------------------------------------------------------------------
-- 4. Attendance Table
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS attendance_select_policy ON attendance;
CREATE POLICY attendance_select_policy ON attendance
    FOR SELECT USING (
        current_app_user_role() IN ('principal', 'teacher')
        OR student_id IN (
            SELECT id FROM students WHERE user_id = current_app_user_id()
        )
        OR student_id IN (
            SELECT student_id FROM parent_student_links 
            WHERE parent_user_id = current_app_user_id()
        )
    );

DROP POLICY IF EXISTS attendance_insert_teacher ON attendance;
CREATE POLICY attendance_insert_teacher ON attendance
    FOR INSERT WITH CHECK (
        current_app_user_role() = 'principal'
        OR (
            current_app_user_role() = 'teacher'
            AND class_id IN (
                SELECT class_id FROM teacher_class_links 
                WHERE teacher_user_id = current_app_user_id()
            )
        )
    );

DROP POLICY IF EXISTS attendance_update_teacher ON attendance;
CREATE POLICY attendance_update_teacher ON attendance
    FOR UPDATE USING (
        current_app_user_role() = 'principal'
        OR (
            current_app_user_role() = 'teacher'
            AND class_id IN (
                SELECT class_id FROM teacher_class_links 
                WHERE teacher_user_id = current_app_user_id()
            )
        )
    );

-- ------------------------------------------------------------------------------
-- 5. Grades / Report Cards Table
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS grades_select_policy ON grades;
CREATE POLICY grades_select_policy ON grades
    FOR SELECT USING (
        current_app_user_role() IN ('principal', 'teacher')
        OR student_id IN (
            SELECT id FROM students WHERE user_id = current_app_user_id()
        )
        OR student_id IN (
            SELECT student_id FROM parent_student_links 
            WHERE parent_user_id = current_app_user_id()
        )
    );

DROP POLICY IF EXISTS grades_insert_update_teacher ON grades;
CREATE POLICY grades_insert_update_teacher ON grades
    FOR ALL USING (
        current_app_user_role() IN ('principal', 'teacher')
    );

-- ------------------------------------------------------------------------------
-- 6. Fee Invoices & Payments (Strict isolation: Parents and Principal only)
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS fee_invoices_select_policy ON fee_invoices;
CREATE POLICY fee_invoices_select_policy ON fee_invoices
    FOR SELECT USING (
        current_app_user_role() = 'principal'
        OR student_id IN (
            SELECT student_id FROM parent_student_links 
            WHERE parent_user_id = current_app_user_id()
        )
    );

DROP POLICY IF EXISTS fee_payments_select_policy ON fee_payments;
CREATE POLICY fee_payments_select_policy ON fee_payments
    FOR SELECT USING (
        current_app_user_role() = 'principal'
        OR invoice_id IN (
            SELECT fi.id FROM fee_invoices fi
            JOIN parent_student_links psl ON psl.student_id = fi.student_id
            WHERE psl.parent_user_id = current_app_user_id()
        )
    );

DROP POLICY IF EXISTS fee_payments_insert_parent ON fee_payments;
CREATE POLICY fee_payments_insert_parent ON fee_payments
    FOR INSERT WITH CHECK (
        current_app_user_role() IN ('principal', 'parent')
    );

-- ------------------------------------------------------------------------------
-- 7. Timetables, Events & Notices
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS timetable_select_all ON timetable_slots;
CREATE POLICY timetable_select_all ON timetable_slots FOR SELECT USING (true);

DROP POLICY IF EXISTS events_select_all ON events;
CREATE POLICY events_select_all ON events FOR SELECT USING (
    target_role = 'all' 
    OR target_role = current_app_user_role()
    OR current_app_user_role() = 'principal'
);

DROP POLICY IF EXISTS notices_select_all ON notices;
CREATE POLICY notices_select_all ON notices FOR SELECT USING (
    audience_role = 'all' 
    OR audience_role = current_app_user_role()
    OR current_app_user_role() = 'principal'
);

DROP POLICY IF EXISTS notices_insert_leadership ON notices;
CREATE POLICY notices_insert_leadership ON notices
    FOR INSERT WITH CHECK (current_app_user_role() IN ('principal', 'teacher'));

-- ------------------------------------------------------------------------------
-- 8. Homework
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS homework_select_all ON homework;
CREATE POLICY homework_select_all ON homework FOR SELECT USING (true);

DROP POLICY IF EXISTS homework_insert_teacher ON homework;
CREATE POLICY homework_insert_teacher ON homework
    FOR INSERT WITH CHECK (current_app_user_role() IN ('principal', 'teacher'));

-- ------------------------------------------------------------------------------
-- 9. Leave Applications
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS leave_select_policy ON leave_applications;
CREATE POLICY leave_select_policy ON leave_applications
    FOR SELECT USING (
        current_app_user_role() IN ('principal', 'teacher')
        OR applicant_user_id = current_app_user_id()
        OR student_id IN (
            SELECT student_id FROM parent_student_links 
            WHERE parent_user_id = current_app_user_id()
        )
    );

DROP POLICY IF EXISTS leave_insert_policy ON leave_applications;
CREATE POLICY leave_insert_policy ON leave_applications
    FOR INSERT WITH CHECK (
        applicant_user_id = current_app_user_id()
        OR current_app_user_role() IN ('student', 'parent')
    );

-- ------------------------------------------------------------------------------
-- 10. Escalation Tickets
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS escalation_select_policy ON escalation_tickets;
CREATE POLICY escalation_select_policy ON escalation_tickets
    FOR SELECT USING (
        current_app_user_role() = 'principal'
        OR requested_by_user_id = current_app_user_id()
        OR target_user_id = current_app_user_id()
    );

DROP POLICY IF EXISTS escalation_insert_policy ON escalation_tickets;
CREATE POLICY escalation_insert_policy ON escalation_tickets
    FOR INSERT WITH CHECK (
        requested_by_user_id = current_app_user_id()
    );

DROP POLICY IF EXISTS escalation_update_leadership ON escalation_tickets;
CREATE POLICY escalation_update_leadership ON escalation_tickets
    FOR UPDATE USING (
        current_app_user_role() IN ('principal', 'teacher')
    );

-- ------------------------------------------------------------------------------
-- 11. Conversation Sessions & Messages
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS conversation_sessions_policy ON conversation_sessions;
CREATE POLICY conversation_sessions_policy ON conversation_sessions
    FOR ALL USING (user_id = current_app_user_id());

DROP POLICY IF EXISTS conversation_messages_policy ON conversation_messages;
CREATE POLICY conversation_messages_policy ON conversation_messages
    FOR ALL USING (
        session_id IN (
            SELECT id FROM conversation_sessions 
            WHERE user_id = current_app_user_id()
        )
    );

-- ------------------------------------------------------------------------------
-- 12. Audit Log (Append-only by system, viewable by Principal)
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS audit_log_select_principal ON audit_log;
CREATE POLICY audit_log_select_principal ON audit_log
    FOR SELECT USING (current_app_user_role() = 'principal');

DROP POLICY IF EXISTS audit_log_insert_all ON audit_log;
CREATE POLICY audit_log_insert_all ON audit_log
    FOR INSERT WITH CHECK (true);
