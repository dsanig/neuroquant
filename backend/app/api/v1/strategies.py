from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.repositories.domain_repository import DomainRepository
from app.schemas.domain import StrategyOut, UserMeOut

router = APIRouter()


@router.get("", response_model=list[StrategyOut])
def list_strategies(_: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> list[StrategyOut]:
    strategies = DomainRepository(db).list_strategies()
    return [StrategyOut.model_validate(s, from_attributes=True) for s in strategies]
