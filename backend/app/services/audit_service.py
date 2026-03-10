from sqlalchemy.orm import Session

from app.models.entities import AuditLog


class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log(
        self,
        *,
        event_type: str,
        entity_type: str,
        entity_id: str,
        payload: dict,
        actor_user_id: str | None = None,
    ) -> None:
        self.db.add(
            AuditLog(
                actor_user_id=actor_user_id,
                event_type=event_type,
                entity_type=entity_type,
                entity_id=entity_id,
                payload=payload,
            )
        )
