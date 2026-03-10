from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.models.entities import OptionContract
from app.repositories.trade_repository import TradeRepository
from app.schemas.domain import RollDetectionResult, TradeOut, UserMeOut
from app.services.audit_service import AuditService
from app.services.roll_detection import RollDetectionService

router = APIRouter()


@router.get("", response_model=list[TradeOut])
def list_trades(_: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> list[TradeOut]:
    trades = TradeRepository(db).list_trades()
    return [TradeOut.model_validate(t, from_attributes=True) for t in trades]


@router.post("/detect-rolls", response_model=RollDetectionResult)
def detect_rolls(user: UserMeOut = Depends(require_roles("admin", "operator")), db: Session = Depends(get_db)) -> RollDetectionResult:
    repo = TradeRepository(db)
    trades = repo.list_trades()
    contracts = {str(c.id): c for c in db.scalars(select(OptionContract)).all()}
    groups = RollDetectionService.assign_roll_groups(trades, contracts)
    repo.save_all(trades)
    AuditService(db).log(
        event_type="trades.roll_detection.executed",
        entity_type="trade",
        entity_id="bulk",
        actor_user_id=user.id,
        payload={"roll_groups_found": groups},
    )
    db.commit()
    return RollDetectionResult(roll_groups_found=groups)
