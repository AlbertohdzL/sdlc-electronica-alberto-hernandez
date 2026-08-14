"""Módulo de detección de anomalías y estrategias de notificación (OCP)."""

from abc import ABC, abstractmethod


class AlertStrategy(ABC):
    """Interfaz abstracta para estrategias de notificación de alertas (DIP / OCP)."""

    @abstractmethod
    def send_alert(self, message: str) -> None:
        """Envía el mensaje de alerta al canal correspondiente."""
        pass


class ConsoleAlertStrategy(AlertStrategy):
    """Estrategia de alerta que imprime en la salida estándar / logs."""

    def send_alert(self, message: str) -> None:
        print(f"[ALERTA] {message}")


class InMemoryAlertStrategy(AlertStrategy):
    """Estrategia de alerta para pruebas e inspección en memoria."""

    def __init__(self) -> None:
        self.alerts: list[str] = []

    def send_alert(self, message: str) -> None:
        self.alerts.append(message)


class AnomalyDetector:
    """Orquesta la evaluación de telemetría contra umbrales configurados."""

    def __init__(self, strategy: AlertStrategy) -> None:
        self._strategy = strategy

    def evaluate(self, sensor_id: str, value: float, threshold: float | None) -> bool:
        """Evalúa si una medición supera el umbral configurado y dispara la alerta."""
        if threshold is None:
            return False

        if value > threshold:
            message = (
                f"Anomalía detectada en sensor '{sensor_id}': "
                f"valor {value} superó el umbral de {threshold}."
            )
            self._strategy.send_alert(message)
            return True

        return False