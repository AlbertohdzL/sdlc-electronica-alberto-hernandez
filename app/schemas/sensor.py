"""Esquemas Pydantic para el recurso Sensor."""

from typing import Literal
from pydantic import BaseModel, Field


class SensorBase(BaseModel):
    """Atributos comunes del sensor."""

    sensor_id: str = Field(..., min_length=3, max_length=50, examples=["TEMP-01"])
    location: str = Field(..., min_length=2, max_length=100, examples=["Pasillo A"])
    sensor_type: Literal["temperature", "humidity"] = Field(
        ..., description="Tipo de sensor soportado"
    )
    alert_threshold: float = Field(..., description="Umbral máximo de alerta")


class SensorCreate(SensorBase):
    """Schema para la creación de un nuevo sensor."""

    pass


class SensorUpdate(BaseModel):
    """Schema para la actualización parcial de un sensor."""

    location: str | None = Field(None, min_length=2, max_length=100)
    alert_threshold: float | None = None
    is_active: bool | None = None


class SensorResponse(SensorBase):
    """Schema de respuesta para la API."""

    id: int
    is_active: bool

    model_config = {"from_attributes": True}