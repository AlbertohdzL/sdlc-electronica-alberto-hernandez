"""Módulo que simula el dispositivo UART físico mediante abstracciones."""

from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.parsers import MessageParser


class UartDevice:
    """Clase de alto nivel que representa el puerto UART.

    Aplica el principio DIP al no depender de un protocolo fijo, sino de
    la abstracción MessageParser inyectada en su inicialización.
    """

    def __init__(self, config: UartConfig, parser: MessageParser) -> None:
        """Inicializa el dispositivo inyectando su configuración y su parser."""
        self.config = config
        self.parser = parser
        self.is_connected: bool = False

    def connect(self) -> None:
        """Simula la apertura del puerto serie físico."""
        self.is_connected = True

    def disconnect(self) -> None:
        """Simula el cierre del puerto serie físico."""
        self.is_connected = False

    def process_incoming_stream(self, raw_data: bytes) -> dict:
        """Recibe un flujo de bytes crudos, valida la conexión y delega el parsing."""
        if not self.is_connected:
            raise RuntimeError("Error de hardware: El puerto UART está cerrado.")

        if not self.parser.can_parse(raw_data):
            raise ValueError("Protocolo no reconocido en el flujo de datos actual.")

        # Delegamos la responsabilidad del procesamiento al parser inyectado
        return self.parser.parse(raw_data)