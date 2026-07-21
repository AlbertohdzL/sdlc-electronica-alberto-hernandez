"""Pruebas unitarias para AnomalyDetector (TDD - US-02)."""

from datetime import datetime
import pytest
from semana2.eval1.anomaly_detector import AnomalyDetector
from semana2.eval1.sensor_reading import SensorReading


def test_detects_temperature_anomaly_when_above_threshold() -> None:
    """Escenario Gherkin 1: Detección de anomalía por alta temperatura (> 35.0 °C)."""
    detector = AnomalyDetector(max_threshold=35.0)
    reading = SensorReading(
        sensor_id="TEMP-02",
        sensor_type="temperature",
        value=36.5,
        unit="C",
        timestamp=datetime.now(),
    )
    assert detector.is_anomaly(reading) is True


def test_normal_reading_returns_false() -> None:
    """Escenario Gherkin 2: Lectura dentro del rango normal (<= umbral)."""
    detector = AnomalyDetector(max_threshold=80.0)
    reading = SensorReading(
        sensor_id="HUM-01",
        sensor_type="humidity",
        value=65.0,
        unit="%",
        timestamp=datetime.now(),
    )
    assert detector.is_anomaly(reading) is False


def test_custom_injected_threshold() -> None:
    """Verifica que el umbral no esté hardcodeado y responda a la inyección."""
    strict_detector = AnomalyDetector(max_threshold=20.0)
    reading = SensorReading(
        sensor_id="TEMP-03",
        sensor_type="temperature",
        value=22.0,
        unit="C",
        timestamp=datetime.now(),
    )
    assert strict_detector.is_anomaly(reading) is True