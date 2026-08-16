import sqlite3
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

DB_PATH = Path(__file__).parent / "school_erp.db"
DATABASE_URL = os.getenv("DATABASE_URL", "")

class UniversalCursor:
    """Cursor wrapper that transparently adapts ? parameter placeholders to %s for PostgreSQL."""
    def __init__(self, raw_cursor, is_postgres: bool = False):
        self._cursor = raw_cursor
        self.is_postgres = is_postgres

    def execute(self, query: str, params: Optional[Any] = None):
        sql = query
        if self.is_postgres:
            sql = sql.replace("?", "%s")
        if params is not None:
            return self._cursor.execute(sql, params)
        return self._cursor.execute(sql)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchmany(self, size: int = 25):
        if hasattr(self._cursor, "fetchmany"):
            return self._cursor.fetchmany(size)
        rows = self._cursor.fetchall()
        return rows[:size] if rows else []

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        return self._cursor.close()

class UniversalConnection:
    """Connection wrapper providing universal SQLite & PostgreSQL database operations."""
    def __init__(self, raw_conn, is_postgres: bool = False):
        self._conn = raw_conn
        self.is_postgres = is_postgres

    def cursor(self):
        return UniversalCursor(self._conn.cursor(), is_postgres=self.is_postgres)

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

    def execute(self, query: str, params: Optional[Any] = None):
        c = self.cursor()
        return c.execute(query, params)

def get_db_connection(db_file: Optional[str] = None):
    """
    Creates a connection to local SQLite or live PostgreSQL/Supabase.
    Returns a unified connection object with row indexing and auto-adapting query syntax.
    """
    if db_file:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return UniversalConnection(conn, is_postgres=False)

    use_local = os.getenv("USE_LOCAL_SQLITE_FALLBACK", "true").lower() == "true"
    if not use_local and DATABASE_URL and DATABASE_URL.startswith("postgres"):
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
            return UniversalConnection(conn, is_postgres=True)
        except Exception as e:
            print(f"[Warning] Failed to connect to PostgreSQL ({e}), falling back to SQLite.")

    path = str(DB_PATH)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return UniversalConnection(conn, is_postgres=False)

def init_db(db_file: Optional[str] = None):
    """Initializes database schema for SQLite or PostgreSQL."""
    path = db_file or str(DB_PATH)
    # If explicitly pointing to SQLite file or fallback
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        auth_id TEXT UNIQUE,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('student', 'parent', 'teacher', 'principal')),
        phone TEXT,
        preferred_language TEXT DEFAULT 'en',
        avatar_url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS classes (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        grade INTEGER NOT NULL,
        section TEXT NOT NULL,
        class_teacher_id TEXT REFERENCES users(id),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS subjects (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        user_id TEXT UNIQUE REFERENCES users(id),
        roll_number TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        class_id TEXT REFERENCES classes(id),
        date_of_birth DATE,
        gender TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS parent_student_links (
        id TEXT PRIMARY KEY,
        parent_user_id TEXT NOT NULL REFERENCES users(id),
        student_id TEXT NOT NULL REFERENCES students(id),
        relationship TEXT DEFAULT 'Parent',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(parent_user_id, student_id)
    );

    CREATE TABLE IF NOT EXISTS teacher_class_links (
        id TEXT PRIMARY KEY,
        teacher_user_id TEXT NOT NULL REFERENCES users(id),
        class_id TEXT NOT NULL REFERENCES classes(id),
        subject_id TEXT REFERENCES subjects(id),
        is_class_teacher INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(teacher_user_id, class_id, subject_id)
    );

    CREATE TABLE IF NOT EXISTS attendance (
        id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL REFERENCES students(id),
        class_id TEXT NOT NULL REFERENCES classes(id),
        date DATE NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('present', 'absent', 'late', 'excused')),
        marked_by TEXT REFERENCES users(id),
        remarks TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(student_id, date)
    );

    CREATE TABLE IF NOT EXISTS exams (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        term TEXT NOT NULL,
        academic_year TEXT NOT NULL,
        start_date DATE,
        end_date DATE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS grades (
        id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL REFERENCES students(id),
        subject_id TEXT NOT NULL REFERENCES subjects(id),
        exam_id TEXT NOT NULL REFERENCES exams(id),
        marks_obtained REAL NOT NULL,
        max_marks REAL NOT NULL DEFAULT 100.0,
        grade TEXT,
        remarks TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(student_id, subject_id, exam_id)
    );

    CREATE TABLE IF NOT EXISTS homework (
        id TEXT PRIMARY KEY,
        class_id TEXT NOT NULL REFERENCES classes(id),
        subject_id TEXT NOT NULL REFERENCES subjects(id),
        teacher_id TEXT NOT NULL REFERENCES users(id),
        title TEXT NOT NULL,
        description TEXT,
        assigned_date DATE NOT NULL,
        due_date DATE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS fee_invoices (
        id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL REFERENCES students(id),
        term TEXT NOT NULL,
        academic_year TEXT NOT NULL,
        total_amount REAL NOT NULL,
        due_date DATE NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('paid', 'partial', 'unpaid', 'overdue')),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS fee_payments (
        id TEXT PRIMARY KEY,
        invoice_id TEXT NOT NULL REFERENCES fee_invoices(id),
        amount_paid REAL NOT NULL,
        payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        payment_method TEXT DEFAULT 'Online UPI',
        receipt_no TEXT UNIQUE NOT NULL,
        transaction_ref TEXT
    );

    CREATE TABLE IF NOT EXISTS timetable_slots (
        id TEXT PRIMARY KEY,
        class_id TEXT NOT NULL REFERENCES classes(id),
        day_of_week TEXT NOT NULL,
        period_number INTEGER NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        subject_id TEXT NOT NULL REFERENCES subjects(id),
        teacher_id TEXT NOT NULL REFERENCES users(id),
        room_number TEXT
    );

    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        event_date DATE NOT NULL,
        event_type TEXT NOT NULL,
        target_role TEXT DEFAULT 'all'
    );

    CREATE TABLE IF NOT EXISTS notices (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        posted_by TEXT REFERENCES users(id),
        target_role TEXT DEFAULT 'all',
        is_urgent INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS leave_applications (
        id TEXT PRIMARY KEY,
        applicant_user_id TEXT NOT NULL REFERENCES users(id),
        applicant_role TEXT NOT NULL,
        student_id TEXT REFERENCES students(id),
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        reason TEXT NOT NULL,
        status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
        approved_by TEXT REFERENCES users(id),
        remarks TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS escalation_tickets (
        id TEXT PRIMARY KEY,
        requested_by_user_id TEXT NOT NULL REFERENCES users(id),
        requested_by_role TEXT NOT NULL,
        student_id TEXT REFERENCES students(id),
        target_entity TEXT NOT NULL,
        target_user_id TEXT REFERENCES users(id),
        reason TEXT NOT NULL,
        status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'failed', 'resolved')),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        resolved_at DATETIME,
        resolution_notes TEXT
    );

    CREATE TABLE IF NOT EXISTS conversation_sessions (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES users(id),
        session_token TEXT UNIQUE NOT NULL,
        language TEXT DEFAULT 'en',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS conversation_messages (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL REFERENCES conversation_sessions(id) ON DELETE CASCADE,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        tool_calls TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS audit_log (
        id TEXT PRIMARY KEY,
        actor_user_id TEXT REFERENCES users(id),
        actor_role TEXT,
        action TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id TEXT,
        details TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Local database schema initialized successfully at:", DB_PATH)
