from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.repositories.domain_repository import DomainRepository
from app.schemas.domain import IncomeEventOut, UserMeOut

router = APIRouter()


@router.get("", response_model=list[IncomeEventOut])
def list_income(_: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> list[IncomeEventOut]:
    events = DomainRepository(db).list_income_events()
    return [IncomeEventOut.model_validate(event, from_attributes=True) for event in events]
