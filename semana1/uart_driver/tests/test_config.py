"""Pruebas unitarias para validar la configuración del driver UART."""

from dataclasses import FrozenInstanceError
import pytest
from semana1.uart_driver.config import UartConfig


def test_valid_config() -> None:
    """Prueba 1: Valida la creación correcta con parámetros estándar."""
    config = UartConfig(baudrate=115200, port="/dev/ttyS0", timeout=2.0)
    assert config.baudrate == 115200
    assert config.port == "/dev/ttyS0"
    assert config.timeout == 2.0


def test_invalid_baudrate_raises_error() -> None:
    """Prueba 2: Verifica que un baudrate no estándar lance un ValueError."""
    with pytest.raises(ValueError):
        # 9601 no es un baudrate comercial estándar
        UartConfig(baudrate=9601)


def test_config_is_frozen() -> None:
    """Prueba 3: Garantiza la inmutabilidad (no se pueden modificar atributos)."""
    config = UartConfig(baudrate=9600)
    with pytest.raises(FrozenInstanceError):
        # Intentar modificar el puerto en caliente debe fallar
        config.port = "/dev/ttyUSB1"  # type: ignore