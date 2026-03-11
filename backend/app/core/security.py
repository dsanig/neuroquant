from datetime import datetime, timedelta, timezone
from uuid import uuid4

import bcrypt
from jose import jwt

from app.core.config import settings

ALGORITHM = "HS256"
BCRYPT_ROUNDS = 12


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def password_needs_rehash(hashed_password: str) -> bool:
    parts = hashed_password.split("$", 3)
    if len(parts) < 3 or not parts[2].isdigit():
        return True
    return int(parts[2]) != BCRYPT_ROUNDS


def validate_password_strength(password: str) -> None:
    if len(password) < 12:
        raise ValueError("password must be at least 12 characters")
    if password.lower() == password or password.upper() == password:
        raise ValueError("password must include uppercase and lowercase characters")
    if not any(char.isdigit() for char in password):
        raise ValueError("password must include at least one digit")
    if password.isalnum():
        raise ValueError("password must include at least one symbol")


def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "nbf": now,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "jti": uuid4().hex,
        "type": "access",
    }
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=ALGORITHM)
