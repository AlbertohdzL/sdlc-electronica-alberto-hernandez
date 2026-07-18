"""Pruebas unitarias para validar el flujo operativo de UartDevice."""

import pytest
from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.device import UartDevice
from semana1.uart_driver.parsers import ModbusParser, NMEAParser


def test_device_connection_flow() -> None:
    """Test 1: Valida que el estado de la conexión cambie correctamente."""
    config = UartConfig(baudrate=9600)
    parser = ModbusParser()
    device = UartDevice(config, parser)

    assert device.is_connected is False
    device.connect()
    assert device.is_connected is True
    device.disconnect()
    assert device.is_connected is False


def test_process_stream_without_connection_raises_error() -> None:
    """Test 2: Comprueba que no se puedan procesar datos si el puerto está cerrado."""
    config = UartConfig(baudrate=9600)
    parser = ModbusParser()
    device = UartDevice(config, parser)

    with pytest.raises(RuntimeError):
        device.process_incoming_stream(b"\x01\x03\x05")


def test_device_routes_to_injected_parser_successfully() -> None:
    """Test 3: Valida que el dispositivo procese datos usando el parser inyectado."""
    config = UartConfig(baudrate=115200)
    
    # Probamos inyectando el parser de NMEA
    nmea_parser = NMEAParser()
    device = UartDevice(config, nmea_parser)
    device.connect()

    raw_nmea = b"$GPGGA,123456,19.432,N,96.913,W,1,08"
    result = device.process_incoming_stream(raw_nmea)

    assert result["protocol"] == "NMEA"
    assert result["latitude"] == "19.432"
    assert result["longitude"] == "96.913"