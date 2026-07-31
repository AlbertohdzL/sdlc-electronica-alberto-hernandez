"""Esquemas Pydantic para las Lecturas de Sensores con validación física."""

from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class ReadingCreate(BaseModel):
    """Schema de entrada para registrar una lectura con validación física estricta."""

    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float = Field(..., description="Valor numérico de la lectura")
    unit: str = Field(..., examples=["C", "%"])
    sensor_type: str = Field(..., examples=["temperature", "humidity"])

    @model_validator(mode="after")
    def validate_physical_limits(self) -> "ReadingCreate":
        """Valida que la unidad y el rango numérico correspondan a física real."""
        stype = self.sensor_type.lower()
        unit = self.unit.upper()

        if stype == "temperature":
            if unit != "C":
                raise ValueError("Para temperatura solo se acepta la unidad 'C'.")
            if not (-50.0 <= self.value <= 100.0):
                raise ValueError(
                    f"Temperatura {self.value} °C fuera de rango físico (-50 a 100 °C)."
                )

        elif stype == "humidity":
            if unit != "%":
                raise ValueError("Para humedad solo se acepta la unidad '%'.")
            if not (0.0 <= self.value <= 100.0):
                raise ValueError(
                    f"Humedad {self.value} % fuera de rango físico (0 a 100 %)."
                )

        else:
            raise ValueError(f"Tipo de sensor '{self.sensor_type}' desconocido.")

        return self


class ReadingResponse(BaseModel):
    """Schema de respuesta para lecturas registradas."""

    id: int
    sensor_id: str
    value: float
    unit: str
    created_at: datetime

    model_config = {"from_attributes": True}