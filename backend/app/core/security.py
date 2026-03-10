from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def password_needs_rehash(hashed_password: str) -> bool:
    return pwd_context.needs_update(hashed_password)


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
