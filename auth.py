from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hashlib
import os

# =========================
# JWT CONFIG
# =========================
SECRET_KEY = os.environ.get(
    "JWT_SECRET_KEY",
    "qwinnet-super-secret-key-change-in-production"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 jam

security = HTTPBearer()

# =========================
# PASSWORD UTILS (SHA256)
# =========================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

# =========================
# ADMIN USER (STATIC)
# =========================
ADMIN_USERS = {
    "admin@qwin.net": {
        "email": "admin@qwin.net",
        # ⬇️ password = admin123
        "hashed_password": hash_password("admin123"),
        "role": "admin"
    }
}

# =========================
# AUTH FUNCTIONS
# =========================
def authenticate_admin(email: str, password: str) -> Optional[dict]:
    user = ADMIN_USERS.get(email)
    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    return user

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        role = payload.get("role")

        if email is None or role != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
