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
        conn = sqlite3.connect(db_file, timeout=20.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout = 5000;")
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
    conn = sqlite3.connect(path, timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 5000;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return UniversalConnection(conn, is_postgres=False)

def init_db(db_file: Optional[str] = None):
    """Initializes database schema for SQLite or PostgreSQL."""
    path = db_file or str(DB_PATH)
    # If explicitly pointing to SQLite file or fallback
    conn = sqlite3.connect(path, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 30000;")
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

def save_conversation_turn(session_id: str, user_id: str, user_msg: str, assistant_reply: str, language: str = 'en', tools: list = None):
    """Persists conversational message turn into database for cross-refresh persistence."""
    try:
        import uuid
        import json
        conn = get_db_connection()
        c = conn.cursor()
        # 1. Ensure conversation session exists (safely checking user reference)
        valid_user_id = None
        if user_id:
            c.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if c.fetchone():
                valid_user_id = user_id

        c.execute("""
            INSERT OR IGNORE INTO conversation_sessions (id, user_id, session_token, language)
            VALUES (?, ?, ?, ?);
        """, (session_id, valid_user_id or user_id or 'usr_guest', session_id, language))
        
        # 2. Update session language and timestamp
        c.execute("""
            UPDATE conversation_sessions
            SET language = ?
            WHERE id = ?;
        """, (language, session_id))
        
        # 3. Insert user message
        user_msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        c.execute("""
            INSERT INTO conversation_messages (id, session_id, role, content, tool_calls)
            VALUES (?, ?, 'user', ?, NULL);
        """, (user_msg_id, session_id, user_msg))
        
        # 4. Insert assistant message
        asst_msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        tools_json = json.dumps(tools) if tools else None
        c.execute("""
            INSERT INTO conversation_messages (id, session_id, role, content, tool_calls)
            VALUES (?, ?, 'assistant', ?, ?);
        """, (asst_msg_id, session_id, assistant_reply, tools_json))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Notice] save_conversation_turn error: {e}")

def get_conversation_history(session_id: str, limit: int = 50) -> list:
    """Retrieves chronological message history for a session."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT role, content, tool_calls, created_at
            FROM conversation_messages
            WHERE session_id = ?
            ORDER BY created_at ASC
            LIMIT ?;
        """, (session_id, limit))
        rows = c.fetchall()
        conn.close()
        
        history = []
        for r in rows:
            if isinstance(r, dict):
                role = r.get("role")
                content = r.get("content")
                created_at = r.get("created_at")
            else:
                role = r[0]
                content = r[1]
                created_at = r[3]
            history.append({
                "role": role,
                "content": content,
                "created_at": str(created_at)
            })
        return history
    except Exception as e:
        print(f"[DB Notice] get_conversation_history error: {e}")
        return []

def get_user_conversation_sessions(user_id: str, limit: int = 30) -> list:
    """Retrieves list of previous chat sessions for a user with preview titles."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT s.id as session_id, s.language, s.created_at,
                   (SELECT content FROM conversation_messages WHERE session_id = s.id AND role = 'user' ORDER BY created_at ASC LIMIT 1) as title,
                   (SELECT content FROM conversation_messages WHERE session_id = s.id ORDER BY created_at DESC LIMIT 1) as last_message,
                   (SELECT COUNT(*) FROM conversation_messages WHERE session_id = s.id) as message_count
            FROM conversation_sessions s
            WHERE s.user_id = ? OR s.id LIKE ?
            ORDER BY s.created_at DESC
            LIMIT ?;
        """, (user_id, f"%{user_id}%", limit))
        rows = c.fetchall()
        conn.close()
        
        sessions = []
        for r in rows:
            if isinstance(r, dict):
                sid = r.get("session_id")
                lang = r.get("language")
                created = r.get("created_at")
                title = r.get("title") or "New Conversation"
                last_msg = r.get("last_message") or ""
                cnt = r.get("message_count") or 0
            else:
                sid, lang, created, title, last_msg, cnt = r[0], r[1], r[2], r[3] or "New Conversation", r[4] or "", r[5] or 0
            
            # Clean preview title length
            clean_title = (title[:48] + "...") if len(title) > 48 else title
            sessions.append({
                "session_id": sid,
                "language": lang or "en",
                "title": clean_title,
                "last_message": last_msg[:60] if last_msg else "",
                "message_count": cnt,
                "created_at": str(created)
            })
        return sessions
    except Exception as e:
        print(f"[DB Notice] get_user_conversation_sessions error: {e}")
        return []

def delete_conversation_session(session_id: str, user_id: str = None) -> bool:
    """Deletes a conversation session and all its messages."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM conversation_messages WHERE session_id = ?", (session_id,))
        if user_id:
            c.execute("DELETE FROM conversation_sessions WHERE id = ? AND (user_id = ? OR user_id IS NULL)", (session_id, user_id))
        else:
            c.execute("DELETE FROM conversation_sessions WHERE id = ?", (session_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB Notice] delete_conversation_session error: {e}")
        return False

def get_user_recent_session(user_id: str) -> Optional[dict]:
    """Retrieves the most recent session for a given user."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT id, language, created_at
            FROM conversation_sessions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1;
        """, (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            if isinstance(row, dict):
                sid = row.get("id")
                lang = row.get("language")
            else:
                sid = row[0]
                lang = row[1]
            return {"session_id": sid, "language": lang}
        return None
    except Exception as e:
        print(f"[DB Notice] get_user_recent_session error: {e}")
        return None

if __name__ == "__main__":
    init_db()
    print("Local database schema initialized successfully at:", DB_PATH)
