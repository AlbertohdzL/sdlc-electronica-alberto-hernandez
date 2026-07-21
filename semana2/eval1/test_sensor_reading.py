"""Pruebas unitarias para la clase SensorReading (TDD - US-01)."""

from datetime import datetime
import pytest
from semana2.eval1.sensor_reading import SensorReading


def test_create_valid_temperature_reading() -> None:
    """Escenario Gherkin 1: Recepción de una lectura válida de temperatura."""
    now = datetime.now()
    reading = SensorReading(
        sensor_id="TEMP-01",
        sensor_type="temperature",
        value=24.5,
        unit="C",
        timestamp=now,
    )
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 24.5
    assert reading.status == "OK"


def test_reject_out_of_bounds_temperature_raises_error() -> None:
    """Escenario Gherkin 2: Rechazo de temperatura bajo el cero absoluto."""
    with pytest.raises(ValueError, match="fuera del rango físico"):
        SensorReading(
            sensor_id="TEMP-01",
            sensor_type="temperature",
            value=-300.0,
            unit="C",
        )


def test_reject_out_of_bounds_humidity_raises_error() -> None:
    """Escenario Gherkin 3: Rechazo de humedad fuera del rango 0% a 100%."""
    with pytest.raises(ValueError, match="fuera del rango físico"):
        SensorReading(
            sensor_id="HUM-01",
            sensor_type="humidity",
            value=110.0,
            unit="%",
        )