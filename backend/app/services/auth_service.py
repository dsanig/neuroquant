from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models.entities import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, email: str, password: str) -> str | None:
        user = self.db.scalar(select(User).where(User.email == email, User.is_active.is_(True)))
        if not user or not verify_password(password, user.password_hash):
            return None
        return create_access_token(str(user.id))
