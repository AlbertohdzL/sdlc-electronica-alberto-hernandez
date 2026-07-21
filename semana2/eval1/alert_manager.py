"""Módulo para la gestión y despacho de alertas con patrón Estrategia (US-03)."""

from abc import ABC, abstractmethod


class AlertStrategy(ABC):
    """Interfaz abstracta para las estrategias de envío de alertas (OCP/DIP)."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Envía un mensaje de alerta a un destino específico."""
        pass


class ConsoleAlertStrategy(AlertStrategy):
    """Estrategia para imprimir alertas en la consola estándar."""

    def send(self, message: str) -> None:
        print(message)


class FileAlertStrategy(AlertStrategy):
    """Estrategia para guardar alertas en un archivo de texto en disco."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def send(self, message: str) -> None:
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(message + "\n")


class AlertManager:
    """Orquestador que despacha alertas usando la estrategia inyectada."""

    def __init__(self, strategy: AlertStrategy) -> None:
        self.strategy = strategy

    def notify(self, message: str) -> None:
        """Despacha el mensaje de alerta mediante la estrategia actual."""
        self.strategy.send(message)