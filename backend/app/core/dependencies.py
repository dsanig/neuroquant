from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.domain import UserMeOut
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserMeOut:
    return AuthService(db).me_from_token(token)


def require_roles(*required_roles: str) -> Callable[[UserMeOut], UserMeOut]:
    def validator(user: UserMeOut = Depends(get_current_user)) -> UserMeOut:
        missing = set(required_roles) - set(user.roles)
        if missing:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return validator
