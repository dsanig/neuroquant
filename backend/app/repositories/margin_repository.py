from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import MarginMetric


class MarginRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_metrics(self) -> list[MarginMetric]:
        return list(self.db.scalars(select(MarginMetric).order_by(MarginMetric.measured_at.desc())).all())
