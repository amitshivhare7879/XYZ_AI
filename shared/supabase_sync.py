"""
XYZ AI — Comprehensive Supabase Cloud Database Migrator & Seed Populator
Populates live Supabase PostgreSQL with Grades 9 to 12, PCMB Streams, 3-Month Attendance Calendar,
Monthly/Quarterly Exam Cycles, and Multi-Quarter Fee Records.
"""

import os
import sys
import datetime
import random
import uuid
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

import psycopg2

def sync_to_supabase():
    db_url = os.getenv("DATABASE_URL")
    if not db_url or not db_url.startswith("postgres"):
        print("[Notice] DATABASE_URL is not set to a PostgreSQL / Supabase connection.")
        return

    print(f"Connecting to Supabase PostgreSQL at: {db_url.split('@')[-1]} ...")
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        # 1. Execute schema.sql
        schema_path = ROOT_DIR / "shared" / "schema.sql"
        print(f"Executing schema from: {schema_path} ...")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        cursor.execute(schema_sql)
        conn.commit()
        print("[OK] Supabase tables and RLS policies created successfully!")

        # 2. Clear old data
        print("Clearing and populating real school dataset (Grades 9-12 PCMB, 3-month calendar)...")
        tables = [
            "audit_log", "conversation_messages", "conversation_sessions",
            "escalation_tickets", "leave_applications", "notices", "events",
            "timetable_slots", "fee_payments", "fee_invoices", "homework",
            "grades", "exams", "attendance", "teacher_class_links",
            "parent_student_links", "students", "subjects", "classes", "users"
        ]
        for table in tables:
            cursor.execute(f"DELETE FROM {table};")
        conn.commit()

        # 3. Leadership & Principal
        principal_id = "00000000-0000-0000-0000-000000000001"
        cursor.execute("""
            INSERT INTO users (id, email, name, role, phone, preferred_language)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (principal_id, "principal@school.edu", "Dr. Rajesh Sharma", "principal", "+91-9876543210", "en"))

        # 4. Subjects (Secondary & PCMB / Commerce)
        subjects_data = [
            ("00000000-0000-0000-0000-000000000011", "Mathematics", "MATH101"),
            ("00000000-0000-0000-0000-000000000012", "General Science", "SCI101"),
            ("00000000-0000-0000-0000-000000000013", "English Core & Literature", "ENG101"),
            ("00000000-0000-0000-0000-000000000014", "Hindi Course-A", "HIN101"),
            ("00000000-0000-0000-0000-000000000015", "Social Science", "SOC101"),
            ("00000000-0000-0000-0000-000000000016", "Computer Applications / IT", "IT101"),
            ("00000000-0000-0000-0000-000000000017", "Physics (Theory & Lab)", "PHY101"),
            ("00000000-0000-0000-0000-000000000018", "Chemistry (Theory & Lab)", "CHEM101"),
            ("00000000-0000-0000-0000-000000000019", "Biology & Biotechnology", "BIO101"),
            ("00000000-0000-0000-0000-000000000020", "Computer Science (Python/SQL)", "CS102"),
            ("00000000-0000-0000-0000-000000000021", "Physical Education & Sports", "PE101"),
            ("00000000-0000-0000-0000-000000000022", "Accountancy", "ACC101"),
            ("00000000-0000-0000-0000-000000000023", "Business Studies", "BST101"),
            ("00000000-0000-0000-0000-000000000024", "Economics", "ECO101")
        ]
        for sid, name, code in subjects_data:
            cursor.execute("INSERT INTO subjects (id, name, code) VALUES (%s, %s, %s)", (sid, name, code))

        # 5. Faculty & Teachers (12 Teachers)
        teacher_names = [
            ("Mrs. Anjali Verma", "anjali.verma@school.edu", "00000000-0000-0000-0000-000000000011"),
            ("Dr. Vikram Malhotra", "vikram.m@school.edu", "00000000-0000-0000-0000-000000000017"),
            ("Mrs. Kavita Singh", "kavita.s@school.edu", "00000000-0000-0000-0000-000000000018"),
            ("Dr. Sneha Kulkarni", "sneha.k@school.edu", "00000000-0000-0000-0000-000000000019"),
            ("Mrs. Sunita Rao", "sunita.rao@school.edu", "00000000-0000-0000-0000-000000000013"),
            ("Mr. Manoj Iyer", "manoj.i@school.edu", "00000000-0000-0000-0000-000000000020"),
            ("Mr. Rakesh Pandey", "rakesh.p@school.edu", "00000000-0000-0000-0000-000000000014"),
            ("Ms. Deepa Nair", "deepa.n@school.edu", "00000000-0000-0000-0000-000000000015"),
            ("Mr. Suresh Joshi", "suresh.j@school.edu", "00000000-0000-0000-0000-000000000022"),
            ("Mrs. Pooja Kapoor", "pooja.k@school.edu", "00000000-0000-0000-0000-000000000023"),
            ("Mr. Arvind Menon", "arvind.m@school.edu", "00000000-0000-0000-0000-000000000024"),
            ("Coach Balwinder Singh", "balwinder.s@school.edu", "00000000-0000-0000-0000-000000000021")
        ]
        teachers = []
        for idx, (tname, email, sub_id) in enumerate(teacher_names):
            tid = f"00000000-0000-0000-0000-00000000002{idx:01d}" if idx < 10 else f"00000000-0000-0000-0000-00000000003{idx-10:01d}"
            teachers.append((tid, tname, email, sub_id))
            cursor.execute("""
                INSERT INTO users (id, email, name, role, phone, preferred_language)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (tid, email, tname, "teacher", f"+91-98765432{idx+11:02d}", "en"))

        # 6. Classes (Grades 9 to 12)
        classes_data = [
            ("00000000-0000-0000-0000-000000000041", "Grade 9-A", 9, "A", teachers[7][0]), # Ms. Deepa Nair
            ("00000000-0000-0000-0000-000000000042", "Grade 9-B", 9, "B", teachers[6][0]), # Mr. Rakesh Pandey
            ("00000000-0000-0000-0000-000000000043", "Grade 10-A", 10, "A", teachers[0][0]), # Mrs. Anjali Verma (Rahul)
            ("00000000-0000-0000-0000-000000000044", "Grade 10-B", 10, "B", teachers[4][0]), # Mrs. Sunita Rao
            ("00000000-0000-0000-0000-000000000045", "Grade 11-Science (PCMB)", 11, "A", teachers[1][0]), # Dr. Vikram Malhotra
            ("00000000-0000-0000-0000-000000000046", "Grade 11-Commerce", 11, "B", teachers[8][0]), # Mr. Suresh Joshi
            ("00000000-0000-0000-0000-000000000047", "Grade 12-Science (PCMB)", 12, "A", teachers[2][0]), # Mrs. Kavita Singh
            ("00000000-0000-0000-0000-000000000048", "Grade 12-Commerce", 12, "B", teachers[9][0]), # Mrs. Pooja Kapoor
        ]
        for cid, cname, grade, sec, cteacher in classes_data:
            cursor.execute("INSERT INTO classes (id, name, grade, section, class_teacher_id) VALUES (%s, %s, %s, %s, %s)",
                           (cid, cname, grade, sec, cteacher))

        # Link Class Teachers & Subject Teachers
        cls_10a_id = classes_data[2][0]
        cls_11p_id = classes_data[4][0]
        cls_12p_id = classes_data[6][0]

        for tid, cid, sid, is_ct in [
            (teachers[0][0], cls_10a_id, subjects_data[0][0], True),
            (teachers[1][0], cls_10a_id, subjects_data[1][0], False),
            (teachers[4][0], cls_10a_id, subjects_data[2][0], False),
            (teachers[1][0], cls_11p_id, subjects_data[6][0], True), # Physics HOD
            (teachers[2][0], cls_11p_id, subjects_data[7][0], False), # Chemistry
            (teachers[0][0], cls_11p_id, subjects_data[0][0], False), # Math
            (teachers[3][0], cls_11p_id, subjects_data[8][0], False), # Biology
            (teachers[2][0], cls_12p_id, subjects_data[7][0], True), # Chemistry HOD
            (teachers[1][0], cls_12p_id, subjects_data[6][0], False), # Physics
            (teachers[0][0], cls_12p_id, subjects_data[0][0], False), # Math
            (teachers[3][0], cls_12p_id, subjects_data[8][0], False), # Biology
        ]:
            cursor.execute("""
                INSERT INTO teacher_class_links (teacher_user_id, class_id, subject_id, is_class_teacher)
                VALUES (%s, %s, %s, %s)
            """, (tid, cid, sid, is_ct))

        # 7. Rahul Patel (Student) & Mr. Amit Patel (Parent)
        rahul_user_id = "00000000-0000-0000-0000-000000000051"
        parent_amit_id = "00000000-0000-0000-0000-000000000061"
        rahul_student_id = "00000000-0000-0000-0000-000000000071"

        cursor.execute("""
            INSERT INTO users (id, email, name, role, phone, preferred_language)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (rahul_user_id, "rahul.patel@student.school.edu", "Rahul Patel", "student", "+91-9876500001", "en"))

        cursor.execute("""
            INSERT INTO users (id, email, name, role, phone, preferred_language)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (parent_amit_id, "amit.patel@gmail.com", "Mr. Amit Patel", "parent", "+91-9876500002", "en"))

        cursor.execute("""
            INSERT INTO students (id, user_id, roll_number, name, class_id, date_of_birth, gender)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (rahul_student_id, rahul_user_id, "10A-01", "Rahul Patel", cls_10a_id, "2010-05-14", "Male"))

        cursor.execute("""
            INSERT INTO parent_student_links (parent_user_id, student_id, relationship)
            VALUES (%s, %s, %s)
        """, (parent_amit_id, rahul_student_id, "Father"))

        cls_09a_id = classes_data[0][0]
        cls_10a_id = classes_data[2][0]
        cls_11p_id = classes_data[4][0]
        cls_11c_id = classes_data[5][0]
        cls_12p_id = classes_data[6][0]
        cls_12c_id = classes_data[7][0]

        # Student Roster Definition across 9-12 PCMB (22 students + Rahul = 23 total)
        roster = [
            # Grade 10-A
            ("00000000-0000-0000-0000-000000000072", "Aarav Sharma", cls_10a_id, "Male", "Mr. Sanjay Sharma", "sanjay.sharma@gmail.com"),
            ("00000000-0000-0000-0000-000000000073", "Diya Mehta", cls_10a_id, "Female", "Mrs. Rekha Mehta", "rekha.mehta@gmail.com"),
            ("00000000-0000-0000-0000-000000000074", "Rohan Gupta", cls_10a_id, "Male", "Mr. Sunil Gupta", "sunil.gupta@gmail.com"),
            ("00000000-0000-0000-0000-000000000075", "Priya Nair", cls_10a_id, "Female", "Mr. K. Nair", "k.nair@gmail.com"),
            ("00000000-0000-0000-0000-000000000076", "Ananya Iyer", cls_10a_id, "Female", "Dr. V. Iyer", "v.iyer@gmail.com"),
            ("00000000-0000-0000-0000-000000000077", "Siddharth Joshi", cls_10a_id, "Male", "Mr. Nitin Joshi", "nitin.j@gmail.com"),
            ("00000000-0000-0000-0000-000000000078", "Tanvi Deshmukh", cls_10a_id, "Female", "Mrs. S. Deshmukh", "deshmukh.s@gmail.com"),
            # Grade 11-Science (PCMB)
            ("00000000-0000-0000-0000-000000000079", "Aditya Singhania", cls_11p_id, "Male", "Mr. Raj Singhania", "singhania.raj@corp.in"),
            ("00000000-0000-0000-0000-000000000080", "Riya Mukherjee", cls_11p_id, "Female", "Dr. A. Mukherjee", "amukherjee@med.in"),
            ("00000000-0000-0000-0000-000000000081", "Varun Chawla", cls_11p_id, "Male", "Mr. M. Chawla", "mchawla@tech.com"),
            ("00000000-0000-0000-0000-000000000082", "Shreya Nambiar", cls_11p_id, "Female", "Mrs. Geeta Nambiar", "geeta.nambiar@gmail.com"),
            ("00000000-0000-0000-0000-000000000083", "Neil Bhatia", cls_11p_id, "Male", "Mr. Vikram Bhatia", "vbhatia@gmail.com"),
            ("00000000-0000-0000-0000-000000000084", "Devika Pillai", cls_11p_id, "Female", "Mr. R. Pillai", "rpillai@gmail.com"),
            # Grade 12-Science (PCMB)
            ("00000000-0000-0000-0000-000000000085", "Karthik Sundaram", cls_12p_id, "Male", "Dr. S. Sundaram", "sundaram.s@iit.in"),
            ("00000000-0000-0000-0000-000000000086", "Pooja Reddy", cls_12p_id, "Female", "Mr. Venkat Reddy", "vreddy@gmail.com"),
            ("00000000-0000-0000-0000-000000000087", "Yashvardhan Rathore", cls_12p_id, "Male", "Maj. K. S. Rathore", "rathore.ks@defense.in"),
            ("00000000-0000-0000-0000-000000000088", "Sneha Banerjee", cls_12p_id, "Female", "Prof. T. Banerjee", "tbanerjee@univ.edu"),
            ("00000000-0000-0000-0000-000000000089", "Arjun Kapoor", cls_12p_id, "Male", "Mr. Anil Kapoor", "anil.k@gmail.com"),
            # Grade 9-A & Commerce
            ("00000000-0000-0000-0000-000000000090", "Kabir Khan", cls_09a_id, "Male", "Mr. Tariq Khan", "tariq.khan@gmail.com"),
            ("00000000-0000-0000-0000-000000000091", "Ishaan Verma", cls_09a_id, "Male", "Mrs. Meera Verma", "meera.v@gmail.com"),
            ("00000000-0000-0000-0000-000000000092", "Dhruv Malhotra", cls_11c_id, "Male", "Mr. Harish Malhotra", "hmalhotra@fin.com"),
            ("00000000-0000-0000-0000-000000000093", "Natasha Goel", cls_12c_id, "Female", "Mr. Alok Goel", "alok.goel@trade.in"),
        ]

        all_students = [(rahul_student_id, "Rahul Patel", cls_10a_id)]

        for idx, (st_id, sname, cid, gender, pname, pemail) in enumerate(roster, start=2):
            su_id = f"00000000-0000-0000-0000-0000000001{idx:02d}"
            pu_id = f"00000000-0000-0000-0000-0000000002{idx:02d}"
            email_clean = sname.lower().replace(" ", ".") + "@student.school.edu"

            cursor.execute("""
                INSERT INTO users (id, email, name, role, phone, preferred_language)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (su_id, email_clean, sname, "student", f"+91-987600{idx:04d}", "en"))

            cursor.execute("""
                INSERT INTO users (id, email, name, role, phone, preferred_language)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (pu_id, pemail, pname, "parent", f"+91-987611{idx:04d}", "en"))

            cursor.execute("""
                INSERT INTO students (id, user_id, roll_number, name, class_id, date_of_birth, gender)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (st_id, su_id, f"ROLL-{idx:02d}", sname, cid, "2010-04-12", gender))

            cursor.execute("""
                INSERT INTO parent_student_links (parent_user_id, student_id, relationship)
                VALUES (%s, %s, %s)
            """, (pu_id, st_id, "Father" if "Mr." in pname or "Dr." in pname else "Mother"))

            all_students.append((st_id, sname, cid))

        # 8. 3-Month Attendance Calendar (Past 91 Days -> Rahul Patel exactly 83 Present / 91 Days = 91.2%)
        end_date = datetime.date(2026, 8, 15)
        school_days = []
        curr = end_date - datetime.timedelta(days=130)
        while curr <= end_date:
            if curr.weekday() < 5:
                holiday_dates = {datetime.date(2026, 5, 23), datetime.date(2026, 6, 17), datetime.date(2026, 7, 29)}
                if curr not in holiday_dates:
                    school_days.append(curr)
            curr += datetime.timedelta(days=1)
        school_days = school_days[-91:]

        rahul_absents = {5, 18, 29, 44, 58, 69, 75, 87}
        random.seed(42)

        for s_idx, (st_id, st_name, cl_id) in enumerate(all_students):
            for d_idx, sday in enumerate(school_days):
                date_str = sday.strftime("%Y-%m-%d")
                if st_id == rahul_student_id:
                    status = "absent" if d_idx in rahul_absents else "present"
                else:
                    rand_val = random.random()
                    status = "present" if rand_val > 0.08 else "absent" if rand_val > 0.03 else "late"

                cursor.execute("""
                    INSERT INTO attendance (student_id, class_id, date, status, marked_by)
                    VALUES (%s, %s, %s, %s, %s)
                """, (st_id, cl_id, date_str, status, teachers[0][0]))

        # 9. Exams (Monthly Unit Tests, Quarterly & Mid-Term)
        exams_data = [
            ("00000000-0000-0000-0000-000000000301", "Monthly Unit Test 1", "Term 1", "2025-2026", "2026-05-10", "2026-05-18"),
            ("00000000-0000-0000-0000-000000000302", "Monthly Unit Test 2", "Term 1", "2025-2026", "2026-06-20", "2026-06-28"),
            ("00000000-0000-0000-0000-000000000303", "First Quarterly Examination", "Term 1", "2025-2026", "2026-07-10", "2026-07-22"),
            ("00000000-0000-0000-0000-000000000304", "Mid-Term Examination 2026", "Term 2", "2025-2026", "2026-08-01", "2026-08-14")
        ]
        for eid, ename, term, yr, sdate, edate in exams_data:
            cursor.execute("""
                INSERT INTO exams (id, name, term, academic_year, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (eid, ename, term, yr, sdate, edate))

        pcmb_subs = [subjects_data[6][0], subjects_data[7][0], subjects_data[0][0], subjects_data[8][0], subjects_data[9][0], subjects_data[2][0]]
        sec_subs = [subjects_data[0][0], subjects_data[1][0], subjects_data[2][0], subjects_data[3][0], subjects_data[4][0], subjects_data[5][0]]

        for st_id, st_name, cl_id in all_students:
            active_subs = pcmb_subs if "11" in cl_id or "12" in cl_id else sec_subs
            for sub_id in active_subs:
                for eid, ename, _, _, _, _ in exams_data:
                    if st_id == rahul_student_id:
                        scores_map = {
                            subjects_data[0][0]: 94.0, subjects_data[1][0]: 88.5, subjects_data[2][0]: 91.0,
                            subjects_data[3][0]: 85.0, subjects_data[4][0]: 89.0, subjects_data[5][0]: 96.0
                        }
                        score = scores_map.get(sub_id, 90.0)
                    else:
                        score = round(random.uniform(70.0, 98.0), 1)

                    grade = "A+" if score >= 90 else "A" if score >= 80 else "B+" if score >= 70 else "B"
                    cursor.execute("""
                        INSERT INTO grades (student_id, subject_id, exam_id, marks_obtained, max_marks, grade, remarks)
                        VALUES (%s, %s, %s, %s, 100.0, %s, 'Consistent academic excellence')
                    """, (st_id, sub_id, eid, score, grade))

        # 10. Fee Invoices (Multi-Quarter Billing)
        fee_cycles = [
            ("Quarter 1 (Apr-Jun 2026)", "Term 1", 45000.0, "2026-04-15", "paid"),
            ("Quarter 2 (Jul-Sep 2026)", "Term 1", 45000.0, "2026-07-15", "paid"),
            ("Quarter 3 (Oct-Dec 2026)", "Term 2", 45000.0, "2026-10-15", "unpaid")
        ]
        for st_id, st_name, cl_id in all_students:
            for term_name, acad_term, amount, due_dt, fstatus in fee_cycles:
                inv_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO fee_invoices (id, student_id, term, academic_year, total_amount, due_date, status)
                    VALUES (%s, %s, %s, '2025-2026', %s, %s, %s)
                """, (inv_id, st_id, term_name, amount, due_dt, fstatus))

                if fstatus == "paid":
                    cursor.execute("""
                        INSERT INTO fee_payments (invoice_id, amount_paid, payment_method, receipt_no, transaction_ref)
                        VALUES (%s, %s, 'Online UPI (HDFC Bank)', %s, %s)
                    """, (inv_id, amount, f"REC-2026-{inv_id[:8].upper()}", f"UPI-TXN-{uuid.uuid4().hex[:8].upper()}"))

        # 11. Notices & Escalations
        cursor.execute("""
            INSERT INTO notices (title, body, posted_by, target_role, is_urgent)
            VALUES 
            ('Mid-Term Report Cards & Parent-Teacher Meeting', 'Parent-Teacher Meeting (PTM) for Grades 9 to 12 will be held on Saturday, August 22, 2026.', %s, 'parent', TRUE),
            ('CBSE Inter-School Science & AI Olympiad Registration', 'Students interested in participating in the National Science & AI Olympiad must submit names by Aug 20.', %s, 'student', FALSE),
            ('Senior Secondary PCMB Practical Lab Schedule', 'Physics and Chemistry practical journal submissions due every Friday before 3:30 PM.', %s, 'student', FALSE)
        """, (principal_id, principal_id, teachers[1][0]))

        cursor.execute("""
            INSERT INTO escalation_tickets (requested_by_user_id, requested_by_role, student_id, target_entity, target_user_id, reason, status, resolution_notes)
            VALUES (%s, 'parent', %s, 'teacher', %s, 'Requesting brief telephone discussion regarding Rahul science practical project group allocation.', 'confirmed', 'Callback scheduled for Aug 16 at 4:00 PM with Mrs. Anjali Verma')
        """, (parent_amit_id, rahul_student_id, teachers[0][0]))

        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] Real School ERP database with Grades 9-12 PCMB records populated to Supabase PostgreSQL!")
    except Exception as e:
        print(f"[Error] Error syncing to Supabase: {e}")

if __name__ == "__main__":
    sync_to_supabase()
