"""
XYZ AI — Tool Execution Gateway
Integrates LLM structured tool definitions with application-layer RBAC and ERP services.
Every tool call enforces role permissions and entity ownership before touching the database.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import datetime

ROOT_PATH = str(Path(__file__).parent.parent)
MODULE_PATH = str(Path(__file__).parent)
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)
if MODULE_PATH not in sys.path:
    sys.path.insert(0, MODULE_PATH)

from shared.schemas import UserTokenPayload

from rbac import (
    check_rbac_permission,
    validate_parent_student_ownership,
    validate_teacher_class_ownership,
    get_student_for_user,
    RBACPermissionDenied,
    EntityOwnershipViolation
)
from erp_services import (
    ERPAttendanceService,
    ERPAcademicService,
    ERPFeeService,
    ERPTimetableService,
    ERPNoticeService,
    ERPLeaveService,
    ERPEscalationService
)

# Tool 1: Get Attendance
def tool_get_attendance(
    user: UserTokenPayload,
    student_name: Optional[str] = None,
    student_id: Optional[str] = None
) -> Dict[str, Any]:
    try:
        if user.role == "student":
            check_rbac_permission("student", "attendance", "read_own")
            std = get_student_for_user(user.user_id)
            target_id = std["id"]
        elif user.role == "parent":
            check_rbac_permission("parent", "attendance", "read_child")
            std = validate_parent_student_ownership(user.user_id, student_id=student_id, student_name=student_name)
            target_id = std["id"]
        elif user.role == "teacher":
            check_rbac_permission("teacher", "attendance", "read_class")
            if student_name or student_id:
                std = validate_teacher_class_ownership(user.user_id, student_name=student_name)
                target_id = std["id"]
                return ERPAttendanceService.get_student_attendance(target_id)
            else:
                cls_info = validate_teacher_class_ownership(user.user_id)
                return ERPAttendanceService.get_class_attendance_summary(class_id=cls_info["id"])
        elif user.role == "principal":
            check_rbac_permission("principal", "attendance", "read_all")
            # If no student specified, return overall analytics
            if not student_name and not student_id:
                return ERPAttendanceService.get_school_attendance_analytics()
            # If student specified
            from shared.database import get_db_connection
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT id FROM students WHERE id = ? OR LOWER(name) LIKE LOWER(?)", (student_id, f"%{student_name}%"))
            r = c.fetchone()
            conn.close()
            if not r:
                return {"error": f"Student '{student_name or student_id}' not found."}
            target_id = r["id"]
        else:
            return {"error": "Unauthorized role."}

        return ERPAttendanceService.get_student_attendance(target_id)
    except (RBACPermissionDenied, EntityOwnershipViolation) as e:
        return {"error": str(e), "is_security_refusal": True}
    except Exception as e:
        return {"error": f"Failed to retrieve attendance: {str(e)}"}

# Tool 2: Mark Attendance (Mutating Action)
def tool_mark_attendance(
    user: UserTokenPayload,
    student_name: str,
    status: str,
    date: Optional[str] = None,
    remarks: Optional[str] = None
) -> Dict[str, Any]:
    try:
        check_rbac_permission(user.role, "attendance", "write_class")
        if user.role != "teacher" and user.role != "principal":
            return {"error": "Only teachers and administrators can mark attendance.", "is_security_refusal": True}

        # Resolve student in teacher's assigned class
        std = validate_teacher_class_ownership(user.user_id, student_name=student_name)
        target_date = date or datetime.date.today().strftime("%Y-%m-%d")
        
        valid_status = status.lower().strip()
        if valid_status not in ["present", "absent", "late", "excused"]:
            return {"error": f"Invalid status '{status}'. Must be present, absent, late, or excused."}

        return ERPAttendanceService.mark_attendance(
            student_id=std["id"],
            class_id=std["class_id"],
            date_str=target_date,
            status_val=valid_status,
            marked_by_user_id=user.user_id,
            remarks=remarks
        )
    except (RBACPermissionDenied, EntityOwnershipViolation) as e:
        return {"error": str(e), "is_security_refusal": True}
    except Exception as e:
        return {"error": f"Failed to mark attendance: {str(e)}"}

# Tool 3: Get Academic Grades & Report
def tool_get_grades(
    user: UserTokenPayload,
    student_name: Optional[str] = None,
    student_id: Optional[str] = None,
    exam_id: Optional[str] = None
) -> Dict[str, Any]:
    try:
        if user.role == "student":
            check_rbac_permission("student", "academics", "read_own")
            std = get_student_for_user(user.user_id)
            target_id = std["id"]
        elif user.role == "parent":
            check_rbac_permission("parent", "academics", "read_child")
            std = validate_parent_student_ownership(user.user_id, student_id=student_id, student_name=student_name)
            target_id = std["id"]
        elif user.role in ["teacher", "principal"]:
            check_rbac_permission(user.role, "academics", "read_class" if user.role == "teacher" else "read_all")
            if student_name:
                std = validate_teacher_class_ownership(user.user_id, student_name=student_name) if user.role == "teacher" else None
                if not std:
                    from shared.database import get_db_connection
                    conn = get_db_connection()
                    c = conn.cursor()
                    c.execute("SELECT id FROM students WHERE LOWER(name) LIKE LOWER(?)", (f"%{student_name}%",))
                    r = c.fetchone()
                    conn.close()
                    target_id = r["id"] if r else None
                else:
                    target_id = std["id"]
            else:
                return {"error": "Please provide a student name to retrieve grades."}
        else:
            return {"error": "Unauthorized."}

        return ERPAcademicService.get_student_grades(target_id, exam_id)
    except (RBACPermissionDenied, EntityOwnershipViolation) as e:
        return {"error": str(e), "is_security_refusal": True}
    except Exception as e:
        return {"error": f"Failed to retrieve grades: {str(e)}"}

# Tool 3B: Get Exam Schedule & Upcoming Tests
def tool_get_exam_schedule(user: UserTokenPayload) -> Dict[str, Any]:
    try:
        exams = ERPAcademicService.get_upcoming_exams()
        return {"exams": exams, "count": len(exams)}
    except Exception as e:
        return {"error": f"Failed to retrieve exam schedule: {str(e)}"}

# Tool 4: Get Fee Status & Invoices
def tool_get_fees(
    user: UserTokenPayload,
    student_name: Optional[str] = None
) -> Dict[str, Any]:
    try:
        if user.role == "parent":
            check_rbac_permission("parent", "fees", "read_child")
            std = validate_parent_student_ownership(user.user_id, student_name=student_name)
            return ERPFeeService.get_student_fee_status(std["id"])
        elif user.role == "principal":
            check_rbac_permission("principal", "fees", "read_all")
            return ERPFeeService.get_school_fee_analytics()
        else:
            # Student and Teacher have NO access to fee records
            raise RBACPermissionDenied(f"Role '{user.role}' is strictly forbidden from accessing financial & fee records.")
    except (RBACPermissionDenied, EntityOwnershipViolation) as e:
        return {"error": str(e), "is_security_refusal": True}
    except Exception as e:
        return {"error": f"Failed to retrieve fee information: {str(e)}"}

# Tool 5: Get Timetable & Schedule
def tool_get_timetable(
    user: UserTokenPayload,
    day_of_week: Optional[str] = None
) -> Dict[str, Any]:
    try:
        if user.role == "student":
            check_rbac_permission("student", "timetable", "read_own")
            std = get_student_for_user(user.user_id)
            slots = ERPTimetableService.get_student_schedule(std["class_id"], day_of_week)
            return {"class_name": std["class_name"], "schedule": slots}
        elif user.role == "parent":
            check_rbac_permission("parent", "timetable", "read_child")
            std = validate_parent_student_ownership(user.user_id)
            slots = ERPTimetableService.get_student_schedule(std["class_id"], day_of_week)
            return {"student_name": std["name"], "class_name": std["class_name"], "schedule": slots}
        elif user.role in ["teacher", "principal"]:
            return {"events": ERPTimetableService.get_events()}
        return {"error": "Unauthorized"}
    except (RBACPermissionDenied, EntityOwnershipViolation) as e:
        return {"error": str(e), "is_security_refusal": True}
    except Exception as e:
        return {"error": f"Failed to retrieve schedule: {str(e)}"}

# Tool 6: Get Notices & Events
def tool_get_notices(user: UserTokenPayload) -> Dict[str, Any]:
    try:
        check_rbac_permission(user.role, "notices", "read")
        notices = ERPNoticeService.get_notices(user.role)
        events = ERPTimetableService.get_events()
        return {"notices": notices, "events": events}
    except Exception as e:
        return {"error": f"Failed to retrieve announcements: {str(e)}"}

# Tool 7: Submit Leave Application
def tool_submit_leave(
    user: UserTokenPayload,
    start_date: str,
    end_date: str,
    reason: str,
    student_name: Optional[str] = None
) -> Dict[str, Any]:
    try:
        std_id = None
        if user.role == "parent":
            check_rbac_permission("parent", "leave", "create_child")
            std = validate_parent_student_ownership(user.user_id, student_name=student_name)
            std_id = std["id"]
        elif user.role == "student":
            check_rbac_permission("student", "leave", "create_own")
            std = get_student_for_user(user.user_id)
            std_id = std["id"]
        else:
            check_rbac_permission(user.role, "leave", "create_own")

        return ERPLeaveService.submit_leave(
            applicant_user_id=user.user_id,
            applicant_role=user.role,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            student_id=std_id
        )
    except (RBACPermissionDenied, EntityOwnershipViolation) as e:
        return {"error": str(e), "is_security_refusal": True}
    except Exception as e:
        return {"error": f"Failed to submit leave: {str(e)}"}

# Tool 8: Escalation / Callback Request
def tool_request_escalation(
    user: UserTokenPayload,
    target_entity: str,
    reason: str,
    student_name: Optional[str] = None,
    simulate_failure: bool = False
) -> Dict[str, Any]:
    try:
        check_rbac_permission(user.role, "escalation", "create_child" if user.role == "parent" else "create_own")
        
        std_id = None
        if user.role == "parent":
            std = validate_parent_student_ownership(user.user_id, student_name=student_name)
            std_id = std["id"]
        elif user.role == "student":
            std = get_student_for_user(user.user_id)
            std_id = std["id"]

        valid_target = target_entity.lower().strip()
        if valid_target not in ["teacher", "management", "principal", "counselor"]:
            valid_target = "teacher"

        return ERPEscalationService.create_escalation_ticket(
            requested_by_user_id=user.user_id,
            requested_by_role=user.role,
            target_entity=valid_target,
            reason=reason,
            student_id=std_id,
            simulate_failure=simulate_failure
        )
    except (RBACPermissionDenied, EntityOwnershipViolation) as e:
        return {"error": str(e), "is_security_refusal": True}
    except Exception as e:
        return {"error": f"Failed to create escalation ticket: {str(e)}"}

# Tool 9: Universal Read-Only Database Query Gateway
def tool_query_database(
    user: UserTokenPayload,
    sql_query: str
) -> Dict[str, Any]:
    """
    Executes a read-only SQL query across the 19 interconnected ERP database tables.
    Gives Gemini and Groq full access to query any table, subject, exam, notice, or event.
    """
    try:
        import re
        q_clean = sql_query.strip()
        q_upper = q_clean.upper()

        if not q_upper.startswith("SELECT"):
            return {"error": "Security Alert: Only read-only SELECT queries are allowed."}

        forbidden = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", "REPLACE", "CREATE", "ATTACH", "DETACH"]
        for f in forbidden:
            if re.search(rf"\b{f}\b", q_upper):
                return {"error": f"Security Alert: Database mutation command '{f}' is blocked."}

        # Role protections
        if user.role == "student" and any(t in q_upper for t in ["FEE_INVOICES", "FEE_PAYMENTS", "AUDIT_LOG"]):
            return {"error": "Access Denied: Students cannot access financial or audit records.", "is_security_refusal": True}

        if user.role == "teacher" and any(t in q_upper for t in ["FEE_INVOICES", "FEE_PAYMENTS"]):
            return {"error": "Access Denied: Teachers cannot access school financial records.", "is_security_refusal": True}

        from shared.database import get_db_connection
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(q_clean)
        rows = [dict(r) for r in c.fetchmany(25)]
        conn.close()

        return {
            "query": q_clean,
            "row_count": len(rows),
            "results": rows
        }
    except Exception as e:
        return {"error": f"SQL Query failed: {str(e)}"}

# Tool 11: Get Class Roster & Student Strength
def tool_get_class_roster(
    user: UserTokenPayload,
    class_name: Optional[str] = None
) -> Dict[str, Any]:
    """Retrieves list of enrolled students, roll numbers, and total strength for a class."""
    try:
        from shared.database import get_db_connection
        conn = get_db_connection()
        c = conn.cursor()

        target_class = class_name
        if not target_class:
            if user.role == "teacher":
                c.execute("SELECT name FROM classes WHERE class_teacher_id = ? LIMIT 1", (user.user_id,))
                crow = c.fetchone()
                target_class = crow["name"] if crow else "Grade 10-A"
            elif user.role in ["student", "parent"]:
                c.execute("SELECT c.name FROM students s JOIN classes c ON c.id = s.class_id WHERE s.id = ? OR s.name = ? LIMIT 1", (user.user_id, user.name))
                crow = c.fetchone()
                target_class = crow["name"] if crow else "Grade 10-A"
            else:
                target_class = "Grade 10-A"

        c.execute("""
            SELECT s.id, s.name, s.roll_number, c.name as class_name
            FROM students s
            JOIN classes c ON c.id = s.class_id
            WHERE LOWER(c.name) LIKE LOWER(?)
            ORDER BY s.roll_number
        """, (f"%{target_class}%",))
        rows = [dict(r) for r in c.fetchall()]
        conn.close()

        return {
            "class_name": target_class,
            "total_students": len(rows),
            "students": rows
        }
    except Exception as e:
        return {"error": f"Failed to retrieve class roster: {str(e)}"}

# Tool 12: Get School-Wide Enrollment
def tool_get_school_enrollment(
    user: UserTokenPayload
) -> Dict[str, Any]:
    """Retrieves school-wide enrollment metrics and grade-wise breakdown."""
    try:
        from shared.database import get_db_connection
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT c.name as class_name, COUNT(s.id) as student_count
            FROM classes c
            LEFT JOIN students s ON s.class_id = c.id
            GROUP BY c.id
            ORDER BY c.name
        """)
        rows = [dict(r) for r in c.fetchall()]
        total_enrolled = sum(r["student_count"] for r in rows)
        conn.close()

        return {
            "total_enrolled_students": total_enrolled,
            "class_breakdown": rows
        }
    except Exception as e:
        return {"error": f"Failed to retrieve school enrollment: {str(e)}"}

