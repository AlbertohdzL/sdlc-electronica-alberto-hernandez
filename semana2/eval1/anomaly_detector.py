"""Módulo para la detección de anomalías en lecturas de sensores (US-02)."""

from semana2.eval1.sensor_reading import SensorReading


class AnomalyDetector:
    """Evalúa si una lectura supera el umbral máximo inyectado."""

    def __init__(self, max_threshold: float) -> None:
        """Inicializa el detector inyectando el umbral superior permitido."""
        self.max_threshold = max_threshold

    def is_anomaly(self, reading: SensorReading) -> bool:
        """Retorna True si el valor de la lectura supera el umbral inyectado."""
        return reading.value > self.max_threshold