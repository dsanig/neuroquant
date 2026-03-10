from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.repositories.domain_repository import DomainRepository
from app.schemas.domain import RiskSummaryOut, UserMeOut
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/summary", response_model=RiskSummaryOut)
def risk_summary(_: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> RiskSummaryOut:
    return AnalyticsService(DomainRepository(db)).risk_summary()
