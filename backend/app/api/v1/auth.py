from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.domain import UserMeOut
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    token = AuthService(db).login(payload.email, payload.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserMeOut)
def me(user: UserMeOut = Depends(get_current_user)) -> UserMeOut:
    return user
