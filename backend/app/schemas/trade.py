from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    symbol: str
    side: str
    quantity: int
    price: float
    executed_at: datetime
    roll_group_id: str | None


class RollDetectionResult(BaseModel):
    roll_groups_found: int
