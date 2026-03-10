from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.rate_limit import InMemoryRateLimiter
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.domain import UserMeOut
from app.services.auth_service import AuthService

router = APIRouter()
_login_limiter = InMemoryRateLimiter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    source_ip = request.client.host if request.client else "unknown"
    _login_limiter.check(
        key=f"auth-login:{source_ip}",
        limit=settings.auth_rate_limit_per_minute,
        window_seconds=60,
        on_violation=lambda: None,
    )
    token = AuthService(db).login(
        payload.email,
        payload.password,
        source_ip=source_ip,
        user_agent=request.headers.get("user-agent"),
    )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserMeOut)
def me(user: UserMeOut = Depends(get_current_user)) -> UserMeOut:
    return user
