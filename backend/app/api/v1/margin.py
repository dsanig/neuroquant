from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.margin_repository import MarginRepository
from app.schemas.margin import MarginMetricOut

router = APIRouter()


@router.get("", response_model=list[MarginMetricOut])
def list_margin_metrics(db: Session = Depends(get_db)) -> list[MarginMetricOut]:
    metrics = MarginRepository(db).list_metrics()
    return [MarginMetricOut.model_validate(m, from_attributes=True) for m in metrics]
