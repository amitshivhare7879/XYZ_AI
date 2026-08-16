"""
XYZ AI — Configuration Management
Loads application settings and cloud credentials from environment variables / .env.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Search for .env at project root or backend folder
ROOT_DIR = Path(__file__).parent.parent
env_paths = [ROOT_DIR / ".env", Path(__file__).parent / ".env"]
for p in env_paths:
    if p.exists():
        load_dotenv(dotenv_path=p)
        break

class Settings:
    # 1. AI Configuration (Google Gemini & Groq Llama)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    # 2. Database Configuration (Supabase Postgres & SQLite)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    USE_LOCAL_SQLITE_FALLBACK: bool = os.getenv("USE_LOCAL_SQLITE_FALLBACK", "true").lower() == "true"

    # 3. Supabase Cloud Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")

    # 4. Authentication & Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "xyz-ai-school-erp-super-secret-key-2026")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours

    # 5. Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
