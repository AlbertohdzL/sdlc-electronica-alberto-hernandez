from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AlertUpdate(BaseModel):
    status: str  # "open", "acknowledged", "resolved"


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: int
    reading_id: int
    value: float
    threshold: float
    status: str
    created_at: datetime