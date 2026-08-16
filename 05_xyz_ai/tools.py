"""
XYZ AI — Tool Execution Gateway
Integrates LLM structured tool definitions with application-layer RBAC and ERP services.
Every tool call enforces role permissions and entity ownership before touching the database.
"""

from typing import Dict, Any, Optional, List
import datetime
from shared.schemas import UserTokenPayload
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

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
            std = validate_teacher_class_ownership(user.user_id, student_name=student_name)
            target_id = std["id"]
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
