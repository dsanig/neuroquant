import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.db.session import get_db
from app.schemas.domain import UserMeOut
from app.services.audit_service import AuditService

router = APIRouter()


class LogLevelUpdateRequest(BaseModel):
    log_level: str = Field(pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")


@router.post("/settings/log-level", response_model=dict)
def update_log_level(
    payload: LogLevelUpdateRequest,
    user: UserMeOut = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> dict:
    logging.getLogger().setLevel(payload.log_level)
    AuditService(db).log(
        event_type="settings.changed",
        entity_type="runtime_setting",
        entity_id="log_level",
        actor_user_id=user.id,
        payload={"new_value": payload.log_level},
    )
    db.commit()
    return {"status": "updated", "log_level": payload.log_level}
