from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Trade


class TradeRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_trades(self) -> list[Trade]:
        return list(self.db.scalars(select(Trade).order_by(Trade.executed_at.desc())).all())

    def save_all(self, trades: list[Trade]) -> None:
        for trade in trades:
            self.db.add(trade)
        self.db.commit()
