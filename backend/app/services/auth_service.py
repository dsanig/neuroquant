from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM, create_access_token, password_needs_rehash, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.domain import UserMeOut
from app.services.audit_service import AuditService


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.audit = AuditService(db)

    def login(self, email: str, password: str, *, source_ip: str | None = None, user_agent: str | None = None) -> str:
        user = self.user_repo.get_active_user_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            self.audit.log(
                event_type="auth.login.failed",
                entity_type="user",
                entity_id=email,
                payload={"source_ip": source_ip, "user_agent": user_agent},
            )
            self.db.commit()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if password_needs_rehash(user.password_hash):
            self.audit.log(
                event_type="auth.password.rehash_required",
                entity_type="user",
                entity_id=str(user.id),
                actor_user_id=str(user.id),
                payload={"source_ip": source_ip},
            )

        token = create_access_token(str(user.id))
        self.audit.log(
            event_type="auth.login.success",
            entity_type="user",
            entity_id=str(user.id),
            actor_user_id=str(user.id),
            payload={"source_ip": source_ip, "user_agent": user_agent},
        )
        self.db.commit()
        return token

    def me_from_token(self, token: str) -> UserMeOut:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[ALGORITHM],
                audience=settings.jwt_audience,
                issuer=settings.jwt_issuer,
                options={"require_sub": True, "require_exp": True, "require_iat": True},
            )
            user_id = payload.get("sub")
            token_type = payload.get("type")
        except JWTError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

        if not user_id or token_type != "access":
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
