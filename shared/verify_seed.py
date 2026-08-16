"""
Seed Data Verification Script
"""
from shared.database import get_db_connection

def verify():
    conn = get_db_connection()
    c = conn.cursor()

    # 1. Users count by role
    c.execute("SELECT role, COUNT(*) as cnt FROM users GROUP BY role")
    print("--- User Counts ---")
    for r in c.fetchall():
        print(f"Role: {r['role']} -> {r['cnt']}")

    # 2. Students & Classes
    c.execute("SELECT COUNT(*) as cnt FROM students")
    print(f"Total Students: {c.fetchone()['cnt']}")

    c.execute("SELECT COUNT(*) as cnt FROM classes")
    print(f"Total Classes: {c.fetchone()['cnt']}")

    # 3. Rahul Patel attendance calculation
    c.execute("""
        SELECT COUNT(*) as total_days,
               SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as present_days,
               SUM(CASE WHEN status='absent' THEN 1 ELSE 0 END) as absent_days
        FROM attendance
        WHERE student_id = 'std_rahul_10a'
    """)
    rahul_att = c.fetchone()
    pct = round((rahul_att['present_days'] / rahul_att['total_days']) * 100, 1)
    print(f"--- Rahul Patel Attendance ---")
    print(f"Total Days: {rahul_att['total_days']}, Present: {rahul_att['present_days']}, Absent: {rahul_att['absent_days']}")
    print(f"Calculated Attendance Percentage: {pct}% (Target from brief: 91.2%)")

    # 4. Rahul Parent link
    c.execute("""
        SELECT u.name as parent_name, s.name as student_name, psl.relationship
        FROM parent_student_links psl
        JOIN users u ON u.id = psl.parent_user_id
        JOIN students s ON s.id = psl.student_id
        WHERE s.id = 'std_rahul_10a'
    """)
    parent_link = c.fetchone()
    print(f"Linked Parent: {parent_link['parent_name']} ({parent_link['relationship']}) -> {parent_link['student_name']}")

    # 5. Grades count
    c.execute("SELECT COUNT(*) as cnt FROM grades")
    print(f"Total Grade records: {c.fetchone()['cnt']}")

    # 6. Fees count
    c.execute("SELECT COUNT(*) as cnt FROM fee_invoices")
    print(f"Total Fee Invoices: {c.fetchone()['cnt']}")

    # 7. Timetable slots count
    c.execute("SELECT COUNT(*) as cnt FROM timetable_slots")
    print(f"Total Timetable Slots: {c.fetchone()['cnt']}")

    conn.close()

if __name__ == "__main__":
    verify()
