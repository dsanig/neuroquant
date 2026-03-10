from datetime import datetime

from pydantic import BaseModel


class AuditFields(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
