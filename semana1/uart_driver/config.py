"""Módulo de configuración inmutable para el driver UART."""

from dataclasses import dataclass

# Lista de baudrates estándar aceptados por la industria electrónica
VALID_BAUDRATES = {9600, 19200, 38400, 57600, 115200}


@dataclass(frozen=True)
class UartConfig:
    """Configuración inmutable de un puerto UART.

    Aplica el principio SRP al encargarse únicamente de almacenar
    y validar los parámetros de inicialización del puerto.
    """

    baudrate: int
    port: str = "/dev/ttyUSB0"
    timeout: float = 1.0

    def __post_init__(self) -> None:
        """Valida los parámetros inmediatamente después de la construcción."""
        if self.baudrate not in VALID_BAUDRATES:
            raise ValueError(
                f"Baudrate {self.baudrate} no soportado. "
                f"Formatos válidos: {VALID_BAUDRATES}"
            )