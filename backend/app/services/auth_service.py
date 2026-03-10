from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM, create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.domain import UserMeOut


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def login(self, email: str, password: str) -> str:
        user = self.user_repo.get_active_user_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token(str(user.id))

    def me_from_token(self, token: str) -> UserMeOut:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
        except JWTError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return UserMeOut(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            roles=self.user_repo.get_role_names(str(user.id)),
        )
