"""Módulo para el modelo y validación de lecturas de sensores (US-01)."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class SensorReading:
    """Representa una lectura individual inmutable de un sensor en la bodega."""

    sensor_id: str
    sensor_type: str
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "OK"

    def __post_init__(self) -> None:
        """Valida que la lectura se encuentre dentro de límites físicos reales."""
        normalized_type = self.sensor_type.lower()

        if normalized_type == "temperature":
            # Rango térmico físico aceptado en bodega (-50°C a 100°C)
            if not (-50.0 <= self.value <= 100.0):
                raise ValueError(
                    f"Temperatura {self.value} °C fuera del rango físico seguro (-50 a 100)."
                )
        elif normalized_type == "humidity":
            # Rango de humedad relativa permitida (0% a 100%)
            if not (0.0 <= self.value <= 100.0):
                raise ValueError(
                    f"Humedad {self.value} % fuera del rango físico seguro (0 a 100)."
                )