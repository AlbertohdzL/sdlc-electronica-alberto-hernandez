from pydantic import BaseModel, ConfigDict


class SensorBase(BaseModel):
    sensor_id: str
    name: str | None = None
    sensor_type: str
    location: str
    alert_threshold: float | None = None


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    name: str | None = None
    sensor_type: str | None = None
    location: str | None = None
    alert_threshold: float | None = None
    is_active: bool | None = None


class SensorResponse(SensorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool = True


# Alias para compatibilidad
SensorOut = SensorResponse


class SensorStats(BaseModel):
    sensor_id: str
    count: int
    min_value: float | None
    max_value: float | None
    avg_value: float | None