"""
XYZ AI — Mock School ERP Service Layer
Direct database query layer and mock external systems integration.
All methods operate on verified user context and produce structured data payloads.
"""

import uuid
import datetime
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path

ROOT_PATH = str(Path(__file__).parent.parent)
MODULE_PATH = str(Path(__file__).parent)
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)
if MODULE_PATH not in sys.path:
    sys.path.insert(0, MODULE_PATH)

from shared.database import get_db_connection

try:
    from rbac import log_audit_event
except ImportError:
    import importlib
    log_audit_event = importlib.import_module("rbac").log_audit_event

class ERPAttendanceService:
    @staticmethod
    def get_student_attendance(student_id: str) -> Dict[str, Any]:
        conn = get_db_connection()
        c = conn.cursor()

        # Student info
        c.execute("""
            SELECT s.id, s.name, s.roll_number, c.name as class_name
            FROM students s
            JOIN classes c ON c.id = s.class_id
            WHERE s.id = ?
        """, (student_id,))
        student = c.fetchone()
        if not student:
            conn.close()
            raise ValueError(f"Student with ID '{student_id}' not found.")

        # Aggregate stats
        c.execute("""
            SELECT 
                COUNT(*) as total_days,
                SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as present_days,
                SUM(CASE WHEN status='absent' THEN 1 ELSE 0 END) as absent_days,
                SUM(CASE WHEN status='late' THEN 1 ELSE 0 END) as late_days,
                SUM(CASE WHEN status='excused' THEN 1 ELSE 0 END) as excused_days
            FROM attendance
            WHERE student_id = ?
        """, (student_id,))
        stats = c.fetchone()

        total = stats["total_days"] or 0
        present = stats["present_days"] or 0
        absent = stats["absent_days"] or 0
        late = stats["late_days"] or 0
        excused = stats["excused_days"] or 0
        percentage = round((present / total * 100), 1) if total > 0 else 0.0

        # Recent 10 records
        c.execute("""
            SELECT date, status, remarks
            FROM attendance
            WHERE student_id = ?
            ORDER BY date DESC
            LIMIT 10
        """, (student_id,))
        recent = [dict(r) for r in c.fetchall()]

        return {
            "student_id": student["id"],
            "student_name": student["name"],
            "roll_number": student["roll_number"],
            "class_name": student["class_name"],
            "total_days": total,
            "present_days": present,
            "absent_days": absent,
            "late_days": late,
            "excused_days": excused,
            "percentage": percentage,
            "recent_records": recent
        }

    @staticmethod
    def get_class_attendance_summary(class_id: str, date_str: Optional[str] = None) -> Dict[str, Any]:
        """Returns the daily roster attendance breakdown for a specific class."""
        conn = get_db_connection()
        c = conn.cursor()

        # Get class info
        c.execute("SELECT id, name FROM classes WHERE id = ?", (class_id,))
        cls = c.fetchone()
        if not cls:
            conn.close()
            return {"error": f"Class '{class_id}' not found."}

        class_name = cls["name"]

        # Get all students in class
        c.execute("SELECT id, name, roll_number FROM students WHERE class_id = ? ORDER BY roll_number", (class_id,))
        students = [dict(r) for r in c.fetchall()]
        total_students = len(students)

        # Target date
        if not date_str:
            c.execute("""
                SELECT a.date FROM attendance a
                JOIN students s ON s.id = a.student_id
                WHERE s.class_id = ?
                ORDER BY a.date DESC LIMIT 1
            """, (class_id,))
            d_row = c.fetchone()
            target_date = d_row["date"] if d_row else "2026-08-16"
        else:
            target_date = date_str

        # Get attendance records for this date
        c.execute("""
            SELECT s.name, a.status, s.roll_number
            FROM students s
            LEFT JOIN attendance a ON a.student_id = s.id AND a.date = ?
            WHERE s.class_id = ?
        """, (target_date, class_id))
        records = c.fetchall()

        present_count = 0
        absent_count = 0
        absent_students = []
        for r in records:
            st = (r["status"] or "present").lower()
            if st == "present":
                present_count += 1
            else:
                absent_count += 1
                absent_students.append(r["name"])

        rate = round((present_count / total_students * 100), 1) if total_students > 0 else 100.0
        conn.close()

        return {
            "class_id": class_id,
            "class_name": class_name,
            "date": target_date,
            "total_students": total_students,
            "present_count": present_count,
            "absent_count": absent_count,
            "attendance_rate": rate,
            "absent_students": absent_students
        }

    @staticmethod
    def mark_attendance(
        student_id: str,
        class_id: str,
        date_str: str,
        status_val: str,
        marked_by_user_id: str,
        remarks: Optional[str] = None
    ) -> Dict[str, Any]:
        conn = get_db_connection()
        c = conn.cursor()

        # Check if student exists
        c.execute("SELECT id, name FROM students WHERE id = ?", (student_id,))
        student = c.fetchone()
        if not student:
            conn.close()
            raise ValueError(f"Student ID '{student_id}' does not exist.")

        att_id = f"att_{student_id}_{date_str}"
        c.execute("""
            INSERT INTO attendance (id, student_id, class_id, date, status, marked_by, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(student_id, date) DO UPDATE SET
                status = excluded.status,
                marked_by = excluded.marked_by,
                remarks = excluded.remarks,
                created_at = CURRENT_TIMESTAMP
        """, (att_id, student_id, class_id, date_str, status_val, marked_by_user_id, remarks or ""))

        conn.commit()
        conn.close()

        # Log mutation audit event
        log_audit_event(
            actor_user_id=marked_by_user_id,
            actor_role="teacher",
            action="mark_attendance",
            entity_type="attendance",
            entity_id=att_id,
            details={"student_name": student["name"], "date": date_str, "status": status_val}
        )

        return {
            "success": True,
            "message": f"Successfully marked {student['name']} as {status_val.upper()} for {date_str}.",
            "attendance_id": att_id,
            "student_name": student["name"],
            "date": date_str,
            "status": status_val
        }

    @staticmethod
    def get_school_attendance_analytics() -> Dict[str, Any]:
        conn = get_db_connection()
        c = conn.cursor()

        # Overall school percentage
        c.execute("""
            SELECT 
                COUNT(*) as total_records,
                SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as total_present,
                SUM(CASE WHEN status='absent' THEN 1 ELSE 0 END) as total_absent
            FROM attendance
        """)
        total_stat = c.fetchone()
        tot = total_stat["total_records"] or 0
        pres = total_stat["total_present"] or 0
        overall_pct = round((pres / tot * 100), 1) if tot > 0 else 0.0

        # Class breakdown
        c.execute("""
            SELECT 
                c.name as class_name,
                COUNT(a.id) as total_records,
                SUM(CASE WHEN a.status='present' THEN 1 ELSE 0 END) as present_count,
                ROUND(AVG(CASE WHEN a.status='present' THEN 1.0 ELSE 0.0 END) * 100, 1) as class_percentage
            FROM classes c
            JOIN attendance a ON a.class_id = c.id
            GROUP BY c.id, c.name
            ORDER BY c.grade, c.section
        """)
        class_breakdown = [dict(r) for r in c.fetchall()]

        # Low attendance students (< 85%)
        c.execute("""
            SELECT 
                s.name as student_name,
                s.roll_number,
                c.name as class_name,
                COUNT(a.id) as total_days,
                SUM(CASE WHEN a.status='present' THEN 1 ELSE 0 END) as present_days,
                ROUND(AVG(CASE WHEN a.status='present' THEN 1.0 ELSE 0.0 END) * 100, 1) as percentage
            FROM students s
            JOIN classes c ON c.id = s.class_id
            JOIN attendance a ON a.student_id = s.id
            GROUP BY s.id, s.name, s.roll_number, c.name
            HAVING percentage < 85.0
            ORDER BY percentage ASC
            LIMIT 10
        """)
        low_att_students = [dict(r) for r in c.fetchall()]

        conn.close()
        return {
            "overall_attendance_percentage": overall_pct,
            "total_records_evaluated": tot,
            "class_breakdown": class_breakdown,
            "low_attendance_alerts": low_att_students
        }


class ERPAcademicService:
    @staticmethod
    def get_student_grades(student_id: str, exam_id: Optional[str] = None) -> Dict[str, Any]:
        conn = get_db_connection()
        c = conn.cursor()

        target_exam = exam_id or "exam_final_2026"
        c.execute("""
            SELECT s.name as student_name, sub.name as subject_name, sub.code as subject_code,
                   e.name as exam_name, g.marks_obtained, g.max_marks, g.grade, g.remarks
            FROM grades g
            JOIN students s ON s.id = g.student_id
            JOIN subjects sub ON sub.id = g.subject_id
            JOIN exams e ON e.id = g.exam_id
            WHERE g.student_id = ? AND g.exam_id = ?
        """, (student_id, target_exam))
        grades = [dict(r) for r in c.fetchall()]

        if not grades:
            # Fallback to any exam
            c.execute("""
                SELECT s.name as student_name, sub.name as subject_name, sub.code as subject_code,
                       e.name as exam_name, g.marks_obtained, g.max_marks, g.grade, g.remarks
                FROM grades g
                JOIN students s ON s.id = g.student_id
                JOIN subjects sub ON sub.id = g.subject_id
                JOIN exams e ON e.id = g.exam_id
                WHERE g.student_id = ?
            """, (student_id,))
            grades = [dict(r) for r in c.fetchall()]

        conn.close()
        if not grades:
            return {"student_id": student_id, "grades": [], "average_percentage": 0.0}

        avg_pct = round(sum(g["marks_obtained"] for g in grades) / (len(grades) * 100.0) * 100, 1)
        return {
            "student_name": grades[0]["student_name"],
            "exam_name": grades[0]["exam_name"],
            "grades": grades,
            "average_percentage": avg_pct
        }

    @staticmethod
    def get_upcoming_exams() -> List[Dict[str, Any]]:
        """Retrieves upcoming and scheduled academic examinations."""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT id, name, exam_type, start_date, end_date, academic_year
            FROM exams
            ORDER BY start_date ASC
        """)
        exams = [dict(r) for r in c.fetchall()]
        conn.close()
        return exams

    @staticmethod
    def get_homework_for_class(class_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT hw.id, hw.title, hw.description, hw.assigned_date, hw.due_date,
                   sub.name as subject_name, u.name as teacher_name
            FROM homework hw
            JOIN subjects sub ON sub.id = hw.subject_id
            JOIN users u ON u.id = hw.teacher_id
            WHERE hw.class_id = ?
            ORDER BY hw.due_date ASC
        """, (class_id,))
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows


class ERPFeeService:
    @staticmethod
    def get_student_fee_status(student_id: str) -> Dict[str, Any]:
        conn = get_db_connection()
        c = conn.cursor()

        c.execute("""
            SELECT s.name as student_name, fi.id as invoice_id, fi.term, fi.academic_year,
                   fi.total_amount, fi.due_date, fi.status
            FROM fee_invoices fi
            JOIN students s ON s.id = fi.student_id
            WHERE fi.student_id = ?
            ORDER BY fi.due_date DESC
        """, (student_id,))
        invoices = [dict(r) for r in c.fetchall()]

        # Payments
        for inv in invoices:
            c.execute("""
                SELECT amount_paid, payment_date, payment_method, receipt_no, transaction_ref
                FROM fee_payments
                WHERE invoice_id = ?
            """, (inv["invoice_id"],))
            inv["payments"] = [dict(p) for p in c.fetchall()]

        conn.close()
        total_due = sum(inv["total_amount"] for inv in invoices if inv["status"] in ["unpaid", "overdue", "partial"])
        return {
            "student_id": student_id,
            "student_name": invoices[0]["student_name"] if invoices else "Student",
            "total_outstanding_dues": total_due,
            "invoices": invoices
        }

    @staticmethod
    def get_school_fee_analytics() -> Dict[str, Any]:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT 
                COUNT(*) as total_invoices,
                SUM(total_amount) as total_billed,
                SUM(CASE WHEN status='paid' THEN total_amount ELSE 0 END) as total_collected,
                SUM(CASE WHEN status IN ('unpaid', 'overdue') THEN total_amount ELSE 0 END) as total_outstanding,
                SUM(CASE WHEN status='overdue' THEN 1 ELSE 0 END) as overdue_count
            FROM fee_invoices
        """)
        stats = dict(c.fetchone())
        conn.close()
        return stats


class ERPTimetableService:
    @staticmethod
    def get_student_schedule(class_id: str, day: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        c = conn.cursor()
        query = """
            SELECT tt.day_of_week, tt.period_number, tt.start_time, tt.end_time,
                   sub.name as subject_name, u.name as teacher_name, tt.room_number
            FROM timetable_slots tt
            JOIN subjects sub ON sub.id = tt.subject_id
            JOIN users u ON u.id = tt.teacher_id
            WHERE tt.class_id = ?
        """
        params = [class_id]
        if day:
            query += " AND LOWER(tt.day_of_week) = LOWER(?)"
            params.append(day)
        query += " ORDER BY tt.day_of_week, tt.period_number"

        c.execute(query, params)
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_events() -> List[Dict[str, Any]]:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id, title, description, event_date, event_type, target_role FROM events ORDER BY event_date ASC")
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows


class ERPNoticeService:
    @staticmethod
    def get_notices(role: str = "all") -> List[Dict[str, Any]]:
        conn = get_db_connection()
        c = conn.cursor()
        if role == "all":
            c.execute("""
                SELECT n.id, n.title, n.body, n.target_role, n.is_urgent, n.created_at, u.name as posted_by_name
                FROM notices n
                LEFT JOIN users u ON u.id = n.posted_by
                ORDER BY n.is_urgent DESC, n.created_at DESC
            """)
        else:
            c.execute("""
                SELECT n.id, n.title, n.body, n.target_role, n.is_urgent, n.created_at, u.name as posted_by_name
                FROM notices n
                LEFT JOIN users u ON u.id = n.posted_by
                WHERE n.target_role = 'all' OR n.target_role = ?
                ORDER BY n.is_urgent DESC, n.created_at DESC
            """, (role,))
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows


class ERPLeaveService:
    @staticmethod
    def submit_leave(
        applicant_user_id: str,
        applicant_role: str,
        start_date: str,
        end_date: str,
        reason: str,
        student_id: Optional[str] = None
    ) -> Dict[str, Any]:
        conn = get_db_connection()
        c = conn.cursor()
        leave_id = f"leave_{uuid.uuid4().hex[:8]}"

        c.execute("""
            INSERT INTO leave_applications (id, applicant_user_id, applicant_role, student_id, start_date, end_date, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (leave_id, applicant_user_id, applicant_role, student_id, start_date, end_date, reason))
        conn.commit()
        conn.close()

        log_audit_event(
            actor_user_id=applicant_user_id,
            actor_role=applicant_role,
            action="submit_leave",
            entity_type="leave_application",
            entity_id=leave_id,
            details={"start_date": start_date, "end_date": end_date, "reason": reason}
        )

        return {
            "leave_id": leave_id,
            "status": "pending",
            "message": "Leave application submitted successfully. It has been routed to the class teacher for review."
        }


class ERPEscalationService:
    @staticmethod
    def create_escalation_ticket(
        requested_by_user_id: str,
        requested_by_role: str,
        target_entity: str,
        reason: str,
        student_id: Optional[str] = None,
        simulate_failure: bool = False
    ) -> Dict[str, Any]:
        """
        Creates an escalation ticket with 3-state guarantee (pending -> confirmed/failed).
        Never claims teacher/management is contacted unless confirmed.
        """
        conn = get_db_connection()
        c = conn.cursor()
        ticket_id = f"esc_{uuid.uuid4().hex[:8]}"

        # Look up assigned class teacher if target is 'teacher' and student_id is present
        target_user_id = None
        target_user_name = "Class Teacher"
        if student_id and target_entity == "teacher":
            c.execute("""
                SELECT u.id, u.name
                FROM students s
                JOIN classes cl ON cl.id = s.class_id
                JOIN users u ON u.id = cl.class_teacher_id
                WHERE s.id = ?
            """, (student_id,))
            teacher_row = c.fetchone()
            if teacher_row:
                target_user_id = teacher_row["id"]
                target_user_name = teacher_row["name"]

        # Step 1: Initial state is 'pending'
        c.execute("""
            INSERT INTO escalation_tickets (id, requested_by_user_id, requested_by_role, student_id, target_entity, target_user_id, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (ticket_id, requested_by_user_id, requested_by_role, student_id, target_entity, target_user_id, reason))
        conn.commit()

        # Step 2: Mock external dispatch service
        if simulate_failure:
            final_status = "failed"
            resolution_notes = "Dispatch service connection timeout."
        else:
            final_status = "confirmed"
            resolution_notes = f"Callback request sent to {target_user_name}."

        c.execute("""
            UPDATE escalation_tickets
            SET status = ?, resolution_notes = ?
            WHERE id = ?
        """, (final_status, resolution_notes, ticket_id))
        conn.commit()
        conn.close()

        log_audit_event(
            actor_user_id=requested_by_user_id,
            actor_role=requested_by_role,
            action="escalation_request",
            entity_type="escalation_ticket",
            entity_id=ticket_id,
            details={"target_entity": target_entity, "status": final_status}
        )

        return {
            "ticket_id": ticket_id,
            "status": final_status,
            "target_entity": target_entity,
            "target_name": target_user_name,
            "reason": reason,
            "confirmed": (final_status == "confirmed")
        }
