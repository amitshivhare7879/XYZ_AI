"""
XYZ AI — Comprehensive School ERP Mock Data Generator & Seeder
Generates full real-world school data for Grades 9, 10, 11, 12 (including PCMB streams),
realistic monthly/quarterly exam terms, 3-month attendance calendar, fee invoices,
timetables, homework, notices, and escalation records.
"""

import uuid
import datetime
import random
from typing import Dict, List, Any
from shared.database import get_db_connection, init_db

def generate_seed_data(db_file=None):
    init_db(db_file)
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    # Clear existing data in reverse dependency order
    tables = [
        "audit_log", "conversation_messages", "conversation_sessions",
        "escalation_tickets", "leave_applications", "notices", "events",
        "timetable_slots", "fee_payments", "fee_invoices", "homework",
        "grades", "exams", "attendance", "teacher_class_links",
        "parent_student_links", "students", "subjects", "classes", "users"
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")

    print("[1/9] Seeding Leadership & Administrative Users...")
    principal_id = "usr_principal_01"
    cursor.execute("""
        INSERT INTO users (id, auth_id, email, name, role, phone, preferred_language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (principal_id, "auth_principal_01", "principal@school.edu", "Dr. Rajesh Sharma", "principal", "+91-9876543210", "en"))

    print("[2/9] Seeding Subjects (Secondary & Senior Secondary PCMB / Commerce)...")
    subjects_data = [
        # Secondary Core (Grades 9 & 10)
        ("sub_math", "Mathematics", "MATH101"),
        ("sub_sci", "General Science", "SCI101"),
        ("sub_eng", "English Core & Literature", "ENG101"),
        ("sub_hin", "Hindi Course-A", "HIN101"),
        ("sub_soc", "Social Science", "SOC101"),
        ("sub_cs", "Computer Applications / IT", "IT101"),
        # Senior Secondary PCMB Stream (Grades 11 & 12)
        ("sub_phy_11", "Physics (Theory & Lab)", "PHY101"),
        ("sub_chem_11", "Chemistry (Theory & Lab)", "CHEM101"),
        ("sub_bio_11", "Biology & Biotechnology", "BIO101"),
        ("sub_cs_11", "Computer Science (Python/SQL)", "CS102"),
        ("sub_pe", "Physical Education & Health", "PE101"),
        # Commerce Stream
        ("sub_acc", "Accountancy", "ACC101"),
        ("sub_bst", "Business Studies", "BST101"),
        ("sub_eco", "Economics", "ECO101")
    ]
    for sid, name, code in subjects_data:
        cursor.execute("INSERT INTO subjects (id, name, code) VALUES (?, ?, ?)", (sid, name, code))

    print("[3/9] Seeding Faculty & Subject Specialist Teachers...")
    teacher_specs = [
        ("usr_teacher_01", "Mrs. Anjali Verma", "anjali.verma@school.edu", "sub_math", "+91-9876543201"),
        ("usr_teacher_02", "Dr. Vikram Malhotra", "vikram.m@school.edu", "sub_phy_11", "+91-9876543202"),
        ("usr_teacher_03", "Mrs. Kavita Singh", "kavita.s@school.edu", "sub_chem_11", "+91-9876543203"),
        ("usr_teacher_04", "Dr. Sneha Kulkarni", "sneha.k@school.edu", "sub_bio_11", "+91-9876543204"),
        ("usr_teacher_05", "Mrs. Sunita Rao", "sunita.rao@school.edu", "sub_eng", "+91-9876543205"),
        ("usr_teacher_06", "Mr. Manoj Iyer", "manoj.i@school.edu", "sub_cs_11", "+91-9876543206"),
        ("usr_teacher_07", "Mr. Rakesh Pandey", "rakesh.p@school.edu", "sub_hin", "+91-9876543207"),
        ("usr_teacher_08", "Ms. Deepa Nair", "deepa.n@school.edu", "sub_soc", "+91-9876543208"),
        ("usr_teacher_09", "Mr. Suresh Joshi", "suresh.j@school.edu", "sub_acc", "+91-9876543209"),
        ("usr_teacher_10", "Mrs. Pooja Kapoor", "pooja.k@school.edu", "sub_bst", "+91-9876543211"),
        ("usr_teacher_11", "Mr. Arvind Menon", "arvind.m@school.edu", "sub_eco", "+91-9876543212"),
        ("usr_teacher_12", "Coach Balwinder Singh", "balwinder.s@school.edu", "sub_pe", "+91-9876543213")
    ]
    for tid, tname, email, sub_id, phone in teacher_specs:
        cursor.execute("""
            INSERT INTO users (id, auth_id, email, name, role, phone, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tid, f"auth_{tid}", email, tname, "teacher", phone, "en"))

    print("[4/9] Seeding Classes (Grades 9, 10, 11-PCMB, 11-Commerce, 12-PCMB, 12-Commerce)...")
    classes_data = [
        ("cls_09a", "Grade 9-A", 9, "A", "usr_teacher_08"), # Ms. Deepa Nair
        ("cls_09b", "Grade 9-B", 9, "B", "usr_teacher_07"), # Mr. Rakesh Pandey
        ("cls_10a", "Grade 10-A", 10, "A", "usr_teacher_01"), # Mrs. Anjali Verma (Rahul's class)
        ("cls_10b", "Grade 10-B", 10, "B", "usr_teacher_05"), # Mrs. Sunita Rao
        ("cls_11_pcmb", "Grade 11-Science (PCMB)", 11, "A", "usr_teacher_02"), # Dr. Vikram Malhotra (Physics HOD)
        ("cls_11_comm", "Grade 11-Commerce", 11, "B", "usr_teacher_09"), # Mr. Suresh Joshi
        ("cls_12_pcmb", "Grade 12-Science (PCMB)", 12, "A", "usr_teacher_03"), # Mrs. Kavita Singh (Chem HOD)
        ("cls_12_comm", "Grade 12-Commerce", 12, "B", "usr_teacher_10"), # Mrs. Pooja Kapoor
    ]
    for cid, cname, grade, sec, cteacher in classes_data:
        cursor.execute("INSERT INTO classes (id, name, grade, section, class_teacher_id) VALUES (?, ?, ?, ?, ?)",
                       (cid, cname, grade, sec, cteacher))

    # Link Subject Teachers to Classes
    teacher_links = [
        # Grade 10-A
        ("usr_teacher_01", "cls_10a", "sub_math", 1),
        ("usr_teacher_02", "cls_10a", "sub_sci", 0),
        ("usr_teacher_05", "cls_10a", "sub_eng", 0),
        ("usr_teacher_07", "cls_10a", "sub_hin", 0),
        ("usr_teacher_08", "cls_10a", "sub_soc", 0),
        ("usr_teacher_06", "cls_10a", "sub_cs", 0),
        # Grade 11-PCMB
        ("usr_teacher_02", "cls_11_pcmb", "sub_phy_11", 1),
        ("usr_teacher_03", "cls_11_pcmb", "sub_chem_11", 0),
        ("usr_teacher_01", "cls_11_pcmb", "sub_math", 0),
        ("usr_teacher_04", "cls_11_pcmb", "sub_bio_11", 0),
        ("usr_teacher_06", "cls_11_pcmb", "sub_cs_11", 0),
        ("usr_teacher_05", "cls_11_pcmb", "sub_eng", 0),
        # Grade 12-PCMB
        ("usr_teacher_03", "cls_12_pcmb", "sub_chem_11", 1),
        ("usr_teacher_02", "cls_12_pcmb", "sub_phy_11", 0),
        ("usr_teacher_01", "cls_12_pcmb", "sub_math", 0),
        ("usr_teacher_04", "cls_12_pcmb", "sub_bio_11", 0),
        ("usr_teacher_06", "cls_12_pcmb", "sub_cs_11", 0),
        ("usr_teacher_05", "cls_12_pcmb", "sub_eng", 0),
        # Commerce
        ("usr_teacher_09", "cls_11_comm", "sub_acc", 1),
        ("usr_teacher_10", "cls_11_comm", "sub_bst", 0),
        ("usr_teacher_11", "cls_11_comm", "sub_eco", 0),
        ("usr_teacher_09", "cls_12_comm", "sub_acc", 1),
        ("usr_teacher_10", "cls_12_comm", "sub_bst", 0),
        ("usr_teacher_11", "cls_12_comm", "sub_eco", 0),
    ]
    for tid, cid, sid, is_ct in teacher_links:
        cursor.execute("""
            INSERT INTO teacher_class_links (id, teacher_user_id, class_id, subject_id, is_class_teacher)
            VALUES (?, ?, ?, ?, ?)
        """, (f"tcl_{tid}_{cid}_{sid}", tid, cid, sid, is_ct))

    print("[5/9] Seeding Students & Linked Parents across Grades 9 to 12...")

    # Key Demo Student: Rahul Patel (Grade 10-A, linked to Mr. Amit Patel)
    cursor.execute("""
        INSERT INTO users (id, auth_id, email, name, role, phone, preferred_language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("usr_student_rahul", "auth_student_rahul", "rahul.patel@student.school.edu", "Rahul Patel", "student", "+91-9876500001", "en"))

    cursor.execute("""
        INSERT INTO users (id, auth_id, email, name, role, phone, preferred_language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("usr_parent_amit", "auth_parent_amit", "amit.patel@gmail.com", "Mr. Amit Patel", "parent", "+91-9876500002", "en"))

    cursor.execute("""
        INSERT INTO students (id, user_id, roll_number, name, class_id, date_of_birth, gender)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("std_rahul_patel", "usr_student_rahul", "10A-01", "Rahul Patel", "cls_10a", "2010-05-14", "Male"))

    cursor.execute("""
        INSERT INTO parent_student_links (id, parent_user_id, student_id, relationship)
        VALUES (?, ?, ?, ?)
    """, ("psl_amit_rahul", "usr_parent_amit", "std_rahul_patel", "Father"))

    # Student roster definition across Grades 9, 10, 11-PCMB, 12-PCMB, and Commerce
    roster = [
        # Grade 10-A Students
        ("std_10a_02", "Aarav Sharma", "cls_10a", "Male", "Mr. Sanjay Sharma", "sanjay.sharma@gmail.com"),
        ("std_10a_03", "Diya Mehta", "cls_10a", "Female", "Mrs. Rekha Mehta", "rekha.mehta@gmail.com"),
        ("std_10a_04", "Rohan Gupta", "cls_10a", "Male", "Mr. Sunil Gupta", "sunil.gupta@gmail.com"),
        ("std_10a_05", "Priya Nair", "cls_10a", "Female", "Mr. K. Nair", "k.nair@gmail.com"),
        ("std_10a_06", "Ananya Iyer", "cls_10a", "Female", "Dr. V. Iyer", "v.iyer@gmail.com"),
        ("std_10a_07", "Siddharth Joshi", "cls_10a", "Male", "Mr. Nitin Joshi", "nitin.j@gmail.com"),
        ("std_10a_08", "Tanvi Deshmukh", "cls_10a", "Female", "Mrs. S. Deshmukh", "deshmukh.s@gmail.com"),
        # Grade 11-PCMB (Senior Secondary Science)
        ("std_11p_01", "Aditya Singhania", "cls_11_pcmb", "Male", "Mr. Raj Singhania", "singhania.raj@corp.in"),
        ("std_11p_02", "Riya Mukherjee", "cls_11_pcmb", "Female", "Dr. A. Mukherjee", "amukherjee@med.in"),
        ("std_11p_03", "Varun Chawla", "cls_11_pcmb", "Male", "Mr. M. Chawla", "mchawla@tech.com"),
        ("std_11p_04", "Shreya Nambiar", "cls_11_pcmb", "Female", "Mrs. Geeta Nambiar", "geeta.nambiar@gmail.com"),
        ("std_11p_05", "Neil Bhatia", "cls_11_pcmb", "Male", "Mr. Vikram Bhatia", "vbhatia@gmail.com"),
        ("std_11p_06", "Devika Pillai", "cls_11_pcmb", "Female", "Mr. R. Pillai", "rpillai@gmail.com"),
        # Grade 12-PCMB (Board Batch)
        ("std_12p_01", "Karthik Sundaram", "cls_12_pcmb", "Male", "Dr. S. Sundaram", "sundaram.s@iit.in"),
        ("std_12p_02", "Pooja Reddy", "cls_12_pcmb", "Female", "Mr. Venkat Reddy", "vreddy@gmail.com"),
        ("std_12p_03", "Yashvardhan Rathore", "cls_12_pcmb", "Male", "Maj. K. S. Rathore", "rathore.ks@defense.in"),
        ("std_12p_04", "Sneha Banerjee", "cls_12_pcmb", "Female", "Prof. T. Banerjee", "tbanerjee@univ.edu"),
        ("std_12p_05", "Arjun Kapoor", "cls_12_pcmb", "Male", "Mr. Anil Kapoor", "anil.k@gmail.com"),
        # Grade 9-A & Commerce
        ("std_09a_01", "Kabir Khan", "cls_09a", "Male", "Mr. Tariq Khan", "tariq.khan@gmail.com"),
        ("std_09a_02", "Ishaan Verma", "cls_09a", "Male", "Mrs. Meera Verma", "meera.v@gmail.com"),
        ("std_11c_01", "Dhruv Malhotra", "cls_11_comm", "Male", "Mr. Harish Malhotra", "hmalhotra@fin.com"),
        ("std_12c_01", "Natasha Goel", "cls_12_comm", "Female", "Mr. Alok Goel", "alok.goel@trade.in"),
    ]

    all_student_records = [("std_rahul_patel", "Rahul Patel", "cls_10a")]

    for idx, (sid, sname, cid, gender, pname, pemail) in enumerate(roster, start=2):
        su_id = f"usr_{sid}"
        pu_id = f"usr_parent_{sid}"
        
        # Student User
        email_clean = sname.lower().replace(" ", ".") + "@student.school.edu"
        cursor.execute("""
            INSERT INTO users (id, auth_id, email, name, role, phone, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (su_id, f"auth_{su_id}", email_clean, sname, "student", f"+91-987600{idx:04d}", "en"))

        # Parent User
        cursor.execute("""
            INSERT INTO users (id, auth_id, email, name, role, phone, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pu_id, f"auth_{pu_id}", pemail, pname, "parent", f"+91-987611{idx:04d}", "en"))

        # Student Profile
        roll_code = f"{cid.upper().replace('CLS_', '')}-{idx:02d}"
        cursor.execute("""
            INSERT INTO students (id, user_id, roll_number, name, class_id, date_of_birth, gender)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sid, su_id, roll_code, sname, cid, "2009-08-20" if "12" in cid else "2010-04-12", gender))

        # Parent Link
        cursor.execute("""
            INSERT INTO parent_student_links (id, parent_user_id, student_id, relationship)
            VALUES (?, ?, ?, ?)
        """, (f"psl_{pu_id}_{sid}", pu_id, sid, "Father" if "Mr." in pname or "Dr." in pname else "Mother"))

        all_student_records.append((sid, sname, cid))

    print("[6/9] Generating 3-Month Real Calendar Attendance (~91.2% for Rahul Patel)...")
    end_date = datetime.date(2026, 8, 20)
    school_days = []
    curr = end_date - datetime.timedelta(days=130)
    while curr <= end_date:
        # Exclude Saturday/Sunday
        if curr.weekday() < 5:
            # Exclude major national school holidays (e.g. Independence Day Eve, Eid, Buddha Purnima)
            holiday_dates = {datetime.date(2026, 5, 23), datetime.date(2026, 6, 17), datetime.date(2026, 7, 29)}
            if curr not in holiday_dates:
                school_days.append(curr)
        curr += datetime.timedelta(days=1)
    school_days = school_days[-91:] # Past 91 working school days

    # Rahul Patel attendance: exactly 83 present / 91 days = 91.2%
    rahul_absents = {5, 18, 29, 44, 58, 69, 75, 87}

    random.seed(42)
    for s_idx, (st_id, st_name, cl_id) in enumerate(all_student_records):
        for d_idx, sday in enumerate(school_days):
            date_str = sday.strftime("%Y-%m-%d")
            
            if st_id == "std_rahul_patel":
                status = "absent" if d_idx in rahul_absents else "present"
            else:
                # 90-95% presence probability
                rand_val = random.random()
                status = "present" if rand_val > 0.08 else "absent" if rand_val > 0.03 else "late"

            cursor.execute("""
                INSERT INTO attendance (id, student_id, class_id, date, status, marked_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (f"att_{st_id}_{date_str}", st_id, cl_id, date_str, status, "usr_teacher_01"))

    print("[7/9] Seeding Comprehensive Exams (Monthly Tests, Quarterly & Mid-Term)...")
    exams_data = [
        ("exam_unit_1", "Monthly Unit Test 1", "Term 1", "2025-2026", "2026-05-10", "2026-05-18"),
        ("exam_unit_2", "Monthly Unit Test 2", "Term 1", "2025-2026", "2026-06-20", "2026-06-28"),
        ("exam_quarterly", "First Quarterly Examination", "Term 1", "2025-2026", "2026-07-10", "2026-07-22"),
        ("exam_midterm", "Mid-Term Examination 2026", "Term 2", "2025-2026", "2026-08-01", "2026-08-14")
    ]
    for eid, ename, term, yr, sdate, edate in exams_data:
        cursor.execute("""
            INSERT INTO exams (id, name, term, academic_year, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (eid, ename, term, yr, sdate, edate))

    # Seed Grade 10-A Subjects & PCMB Subjects
    pcmb_subjects = ["sub_phy_11", "sub_chem_11", "sub_math", "sub_bio_11", "sub_cs_11", "sub_eng"]
    sec_subjects = ["sub_math", "sub_sci", "sub_eng", "sub_hin", "sub_soc", "sub_cs"]

    for st_id, st_name, cl_id in all_student_records:
        active_subs = pcmb_subjects if "11" in cl_id or "12" in cl_id else sec_subjects
        for sub_id in active_subs:
            for eid, ename, _, _, _, _ in exams_data:
                if st_id == "std_rahul_patel":
                    marks_dict = {
                        "sub_math": 94.0, "sub_sci": 88.5, "sub_eng": 91.0,
                        "sub_hin": 85.0, "sub_soc": 89.0, "sub_cs": 96.0
                    }
                    score = marks_dict.get(sub_id, 90.0)
                else:
                    score = round(random.uniform(70.0, 98.0), 1)

                grade = "A+" if score >= 90 else "A" if score >= 80 else "B+" if score >= 70 else "B"
                cursor.execute("""
                    INSERT INTO grades (id, student_id, subject_id, exam_id, marks_obtained, max_marks, grade, remarks)
                    VALUES (?, ?, ?, ?, ?, 100.0, ?, 'Consistent academic excellence')
                """, (f"grd_{st_id}_{sub_id}_{eid}", st_id, sub_id, eid, score, grade))

    print("[8/9] Seeding Monthly & Quarterly School Fee Invoices & Payments...")
    fee_cycles = [
        ("inv_q1", "Quarter 1 (Apr-Jun 2026)", "Term 1", 45000.0, "2026-04-15", "paid"),
        ("inv_q2", "Quarter 2 (Jul-Sep 2026)", "Term 1", 45000.0, "2026-07-15", "paid"),
        ("inv_q3", "Quarter 3 (Oct-Dec 2026)", "Term 2", 45000.0, "2026-10-15", "unpaid"),
    ]
    for st_id, st_name, cl_id in all_student_records:
        for fid_prefix, term_name, acad_term, amount, due_dt, fstatus in fee_cycles:
            inv_id = f"{fid_prefix}_{st_id}"
            cursor.execute("""
                INSERT INTO fee_invoices (id, student_id, term, academic_year, total_amount, due_date, status)
                VALUES (?, ?, ?, '2025-2026', ?, ?, ?)
            """, (inv_id, st_id, term_name, amount, due_dt, fstatus))

            if fstatus == "paid":
                cursor.execute("""
                    INSERT INTO fee_payments (id, invoice_id, amount_paid, payment_method, receipt_no, transaction_ref)
                    VALUES (?, ?, ?, 'Online UPI (HDFC Bank)', ?, ?)
                """, (f"pay_{inv_id}", inv_id, amount, f"REC-2026-{uuid.uuid4().hex[:10].upper()}", f"UPI-TXN-{uuid.uuid4().hex[:8].upper()}"))

    print("[9/9] Seeding Timetables, Notices, Events, Homework, & Escalations...")
    # Timetable for Grade 10-A (Monday to Friday, 8 Periods)
    periods = [
        (1, "08:30", "09:15", "sub_math", "usr_teacher_01", "Room 204"),
        (2, "09:15", "10:00", "sub_sci", "usr_teacher_02", "Physics Lab A"),
        (3, "10:15", "11:00", "sub_eng", "usr_teacher_05", "Room 204"),
        (4, "11:00", "11:45", "sub_hin", "usr_teacher_07", "Room 204"),
        (5, "12:30", "01:15", "sub_soc", "usr_teacher_08", "Room 204"),
        (6, "01:15", "02:00", "sub_cs", "usr_teacher_06", "Computer Lab 2"),
        (7, "02:00", "02:45", "sub_sci", "usr_teacher_03", "Chemistry Lab B"),
        (8, "02:45", "03:30", "sub_pe", "usr_teacher_12", "Sports Complex")
    ]
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        for pnum, stime, etime, sub_id, tid, room in periods:
            cursor.execute("""
                INSERT INTO timetable_slots (id, class_id, day_of_week, period_number, start_time, end_time, subject_id, teacher_id, room_number)
                VALUES (?, 'cls_10a', ?, ?, ?, ?, ?, ?, ?)
            """, (f"tt_10a_{day[:3]}_{pnum}", day, pnum, stime, etime, sub_id, tid, room))

    # School Notices & Events
    cursor.execute("""
        INSERT INTO notices (id, title, body, posted_by, target_role, is_urgent)
        VALUES 
        ('not_01', 'Mid-Term Report Cards & Parent-Teacher Meeting', 'Parent-Teacher Meeting (PTM) for Grades 9 to 12 will be held on Saturday, August 22, 2026.', 'usr_principal_01', 'parent', 1),
        ('not_02', 'CBSE Inter-School Science & AI Olympiad Registration', 'Students interested in participating in the National Science & AI Olympiad must submit names by Aug 20.', 'usr_principal_01', 'student', 0),
        ('not_03', 'Senior Secondary PCMB Practical Lab Schedule', 'Physics and Chemistry practical journal submissions due every Friday before 3:30 PM.', 'usr_teacher_02', 'student', 0)
    """)

    cursor.execute("""
        INSERT INTO events (id, title, description, event_date, event_type, target_role)
        VALUES 
        ('evt_01', 'Annual Science & Robotics Fair 2026', 'Inter-house exhibition showcasing PCMB laboratory models and AI projects.', '2026-08-28', 'Academic', 'all'),
        ('evt_02', 'Term 2 Parent Teacher Interaction', 'Discussion on student attendance, unit test progress, and board prep.', '2026-08-22', 'Meeting', 'parent')
    """)

    # Escalation Tickets
    cursor.execute("""
        INSERT INTO escalation_tickets (id, requested_by_user_id, requested_by_role, student_id, target_entity, target_user_id, reason, status, resolution_notes)
        VALUES 
        ('tkt_01', 'usr_parent_amit', 'parent', 'std_rahul_patel', 'teacher', 'usr_teacher_01', 'Requesting brief telephone discussion regarding Rahul science practical project group allocation.', 'confirmed', 'Callback scheduled for Aug 16 at 4:00 PM with Mrs. Anjali Verma')
    """)

    conn.commit()
    conn.close()
    print("[OK] Real School ERP database populated successfully with Grades 9-12 PCMB records!")

if __name__ == "__main__":
    generate_seed_data()
