from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.repositories.domain_repository import DomainRepository
from app.schemas.domain import ImportBatchOut, UserMeOut

router = APIRouter()


@router.get("", response_model=list[ImportBatchOut])
def list_imports(_: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ImportBatchOut]:
    batches = DomainRepository(db).list_import_batches()
    return [ImportBatchOut.model_validate(batch, from_attributes=True) for batch in batches]
