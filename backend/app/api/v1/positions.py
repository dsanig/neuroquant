from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.repositories.domain_repository import DomainRepository
from app.schemas.domain import PositionOut, UserMeOut

router = APIRouter()


@router.get("", response_model=list[PositionOut])
def list_positions(_: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> list[PositionOut]:
    positions = DomainRepository(db).list_positions()
    return [PositionOut.model_validate(p, from_attributes=True) for p in positions]
