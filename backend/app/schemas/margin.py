from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MarginMetricOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    measured_at: datetime
    strategy_id: str | None
    notional_exposure: float
    margin_used: float
    broker_requirement: float | None
    source: str
