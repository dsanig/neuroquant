from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.db.session import get_db
from app.repositories.domain_repository import DomainRepository
from app.schemas.domain import AuditLogOut, UserMeOut

router = APIRouter()


@router.get("", response_model=list[AuditLogOut])
def list_audit_logs(_: UserMeOut = Depends(require_roles("admin", "auditor")), db: Session = Depends(get_db)) -> list[AuditLogOut]:
    logs = DomainRepository(db).list_audit_logs()
    return [AuditLogOut.model_validate(log, from_attributes=True) for log in logs]
