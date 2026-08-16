"""
XYZ AI — Deterministic Application-Layer RBAC & Entity Ownership Validator
Enforces access control entirely in code before tool execution.
Protects against prompt injection, fake role claims, and unauthorized data mutations.
"""

import json
import uuid
from typing import Optional, Dict, Any, List
from shared.database import get_db_connection
from shared.schemas import UserRole

class RBACPermissionDenied(Exception):
    """Raised when user role lacks permission for a domain action."""
    pass

class EntityOwnershipViolation(Exception):
    """Raised when user lacks ownership over target student or class entity."""
    pass

# Formalized Role x Domain Action Permission Matrix
PERMISSIONS: Dict[UserRole, Dict[str, List[str]]] = {
    "student": {
        "attendance": ["read_own"],
        "academics": ["read_own"],
        "fees": [], # Denied
        "timetable": ["read_own"],
        "notices": ["read"],
        "leave": ["create_own", "read_own"],
        "escalation": ["create_own", "read_own"]
    },
    "parent": {
        "attendance": ["read_child"],
        "academics": ["read_child"],
        "fees": ["read_child", "pay_child"],
        "timetable": ["read_child"],
        "notices": ["read"],
        "leave": ["create_child", "read_child"],
        "escalation": ["create_child", "read_child"]
    },
    "teacher": {
        "attendance": ["read_class", "write_class"],
        "academics": ["read_class", "write_class"],
        "fees": [], # Denied
        "timetable": ["read_schedule"],
        "notices": ["read", "create_class"],
        "leave": ["read_class", "approve_class"],
        "escalation": ["read_assigned", "create_admin"]
    },
    "principal": {
        "attendance": ["read_all", "analytics"],
        "academics": ["read_all", "analytics"],
        "fees": ["read_all", "analytics"],
        "timetable": ["read_all", "manage"],
        "notices": ["read", "create_all", "manage"],
        "leave": ["read_all", "approve_all"],
        "escalation": ["read_all", "manage"]
    }
}

def check_rbac_permission(role: UserRole, domain: str, action: str):
    """Validates if the user's verified role possesses permission for domain action."""
    role_domain = PERMISSIONS.get(role, {}).get(domain, [])
    if action not in role_domain and "read_all" not in role_domain and "manage" not in role_domain:
        raise RBACPermissionDenied(
            f"Security Alert: Role '{role}' is not authorized to perform action '{action}' on domain '{domain}'."
        )

def validate_parent_student_ownership(
    parent_user_id: str,
    student_id: Optional[str] = None,
    student_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Ensures a parent user only accesses data of their officially linked child.
    Smartly resolves single-child parents automatically and handles first-name / fuzzy matches.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, s.name, s.roll_number, s.class_id, c.name as class_name
        FROM parent_student_links psl
        JOIN students s ON s.id = psl.student_id
        JOIN classes c ON c.id = s.class_id
        WHERE psl.parent_user_id = ?
    """, (parent_user_id,))
    linked_children = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not linked_children:
        raise EntityOwnershipViolation(
            f"Authorization Error: Parent (ID: {parent_user_id}) does not have linked ownership for requested student."
        )

    # If parent only has 1 child, default to that child automatically unless querying another specific child
    if len(linked_children) == 1 and (not student_name or any(w in student_name.lower() for w in ["child", "son", "daughter", "kid", "my", linked_children[0]["name"].split()[0].lower()])):
        return linked_children[0]

    # If specific student_id provided
    if student_id:
        for child in linked_children:
            if child["id"] == student_id or child["roll_number"].lower() == student_id.lower():
                return child
        raise EntityOwnershipViolation(
            f"Access Denied: You do not have parent authorization for student ID '{student_id}'."
        )

    # If specific student_name provided
    if student_name:
        sname_clean = student_name.lower().strip()
        # Direct match or partial match
        for child in linked_children:
            c_full = child["name"].lower()
            c_first = c_full.split()[0]
            if sname_clean in c_full or c_first in sname_clean or sname_clean[:3] == c_first[:3]:
                return child
        
        # If still only 1 child linked to parent, return that child
        if len(linked_children) == 1:
            return linked_children[0]

        child_names = ", ".join([c["name"] for c in linked_children])
        raise EntityOwnershipViolation(
            f"Could not match '{student_name}'. Your linked children on file: {child_names}."
        )

    # Default to first linked child
    return linked_children[0]

def validate_teacher_class_ownership(teacher_user_id: str, class_id: Optional[str] = None, student_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Ensures a teacher only accesses or marks data for students in their assigned classes.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if student_name:
        # Find student in classes taught by this teacher
        cursor.execute("""
            SELECT s.id, s.name, s.roll_number, s.class_id, c.name as class_name
            FROM students s
            JOIN classes c ON c.id = s.class_id
            JOIN teacher_class_links tcl ON tcl.class_id = s.class_id
            WHERE tcl.teacher_user_id = ? AND LOWER(s.name) LIKE LOWER(?)
        """, (teacher_user_id, f"%{student_name}%"))
        matches = cursor.fetchall()
        conn.close()

        if not matches:
            raise EntityOwnershipViolation(
                f"Authorization Error: Teacher does not teach any student named '{student_name}'."
            )
        if len(matches) > 1:
            names = [f"{m['name']} ({m['class_name']})" for m in matches]
            raise ValueError(f"Ambiguous student name '{student_name}'. Multiple matches found: {', '.join(names)}. Please specify class or roll number.")
        return dict(matches[0])

    if class_id:
        cursor.execute("""
            SELECT c.id, c.name, tcl.is_class_teacher
            FROM teacher_class_links tcl
            JOIN classes c ON c.id = tcl.class_id
            WHERE tcl.teacher_user_id = ? AND (c.id = ? OR LOWER(c.name) = LOWER(?))
        """, (teacher_user_id, class_id, class_id))
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise EntityOwnershipViolation(
                f"Authorization Error: Teacher is not assigned to class '{class_id}'."
            )
        return dict(row)

    # Return primary assigned class
    cursor.execute("""
        SELECT c.id, c.name, tcl.is_class_teacher
        FROM teacher_class_links tcl
        JOIN classes c ON c.id = tcl.class_id
        WHERE tcl.teacher_user_id = ?
        LIMIT 1
    """, (teacher_user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise EntityOwnershipViolation("Teacher has no assigned classes.")
    return dict(row)

def get_student_for_user(student_user_id: str) -> Dict[str, Any]:
    """Retrieves student record linked to student user login."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.name, s.roll_number, s.class_id, c.name as class_name
        FROM students s
        JOIN classes c ON c.id = s.class_id
        WHERE s.user_id = ?
    """, (student_user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise EntityOwnershipViolation(f"No student record found for user {student_user_id}")
    return dict(row)

def log_audit_event(
    actor_user_id: str,
    actor_role: str,
    action: str,
    entity_type: str,
    entity_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """Writes an immutable security & operations audit trail."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_log (id, actor_user_id, actor_role, action, entity_type, entity_id, details)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        f"aud_{uuid.uuid4().hex[:12]}",
        actor_user_id,
        actor_role,
        action,
        entity_type,
        entity_id,
        json.dumps(details or {})
    ))
    conn.commit()
    conn.close()
