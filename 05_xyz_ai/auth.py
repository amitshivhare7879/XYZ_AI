"""
XYZ AI — Authentication & Token Management
Extracts and cryptographically verifies user identity and role from JWT tokens.
Supports Supabase Auth JWTs, Supabase client verification, and custom role claims.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

ROOT_PATH = str(Path(__file__).parent.parent)
MODULE_PATH = str(Path(__file__).parent)
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)
if MODULE_PATH not in sys.path:
    sys.path.insert(0, MODULE_PATH)

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from shared.schemas import UserTokenPayload, UserRole, SupportedLanguage
from shared.database import get_db_connection

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "xyz-ai-school-erp-super-secret-key-2026")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

security = HTTPBearer(auto_error=False)

def create_access_token(payload: UserTokenPayload, expires_delta: Optional[timedelta] = None) -> str:
    """Generates a signed JWT token containing verified user claims."""
    to_encode = payload.model_dump()
    now_utc = datetime.now(timezone.utc)
    if expires_delta:
        expire = now_utc + expires_delta
    else:
        expire = now_utc + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": now_utc})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> UserTokenPayload:
    """
    Decodes and cryptographically validates the JWT token.
    Tries internal secret first, then Supabase JWT secret if configured.
    """
    secrets_to_try = [JWT_SECRET_KEY]
    if SUPABASE_JWT_SECRET and SUPABASE_JWT_SECRET != JWT_SECRET_KEY:
        secrets_to_try.append(SUPABASE_JWT_SECRET)

    last_error = None
    for secret in secrets_to_try:
        try:
            payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM], options={"verify_aud": False})
            
            # Handle standard custom payload or Supabase Auth payload
            user_id = payload.get("user_id") or payload.get("sub")
            email = payload.get("email", "")
            name = payload.get("name") or payload.get("user_metadata", {}).get("name") or email.split("@")[0]
            
            # Role resolution from verified claim or user_metadata
            role = payload.get("role") or payload.get("user_metadata", {}).get("role") or payload.get("app_metadata", {}).get("role")
            
            if not role or role not in ["student", "parent", "teacher", "principal"]:
                # Lookup user in database if not embedded in token claims
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("SELECT role, name, preferred_language FROM users WHERE id = ? OR auth_id = ? OR email = ?", (user_id, user_id, email))
                row = c.fetchone()
                conn.close()
                if row:
                    role = row["role"]
                    name = row["name"]
                    lang = row["preferred_language"] or "en"
                else:
                    role = "parent"
                    lang = "en"
            else:
                lang = payload.get("preferred_language", "en")

            return UserTokenPayload(
                user_id=user_id,
                email=email,
                name=name,
                role=role,
                preferred_language=lang
            )
        except JWTError as e:
            last_error = e

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Token verification failed: {str(last_error)}"
    )

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    authorization: Optional[str] = Header(None)
) -> UserTokenPayload:
    """FastAPI dependency to extract verified user from Authorization Bearer token."""
    token = None
    if credentials:
        token = credentials.credentials
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]

    if not token:
        if os.getenv("ALLOW_DEMO_DEFAULT_AUTH", "false").lower() == "true":
            return UserTokenPayload(
                user_id="usr_parent_amit",
                email="amit.patel@gmail.com",
                name="Mr. Amit Patel",
                role="parent",
                preferred_language="en"
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization Bearer token"
        )
    return decode_access_token(token)

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    authorization: Optional[str] = Header(None)
) -> Optional[UserTokenPayload]:
    """FastAPI dependency to extract user if token is provided, without throwing 401."""
    token = None
    if credentials:
        token = credentials.credentials
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]

    if not token:
        return None
    try:
        return decode_access_token(token)
    except Exception:
        return None

def require_role(*allowed_roles: UserRole):
    """Dependency factory ensuring current user has one of the allowed roles."""
    def role_checker(user: UserTokenPayload = Depends(get_current_user)) -> UserTokenPayload:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Role '{user.role}' is not authorized. Required: {allowed_roles}"
            )
        return user
    return role_checker
