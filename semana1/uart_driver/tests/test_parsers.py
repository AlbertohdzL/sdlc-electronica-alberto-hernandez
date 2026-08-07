"""Pruebas unitarias para validar los parsers de protocolos Modbus y NMEA."""

import pytest
from semana1.uart_driver.parsers import ModbusParser, NMEAParser


# --- TESTS MODBUS PARSER ---
def test_modbus_can_parse_valid_and_invalid() -> None:
    """Test 1: Verifica la discriminación correcta de tramas binarias."""
    parser = ModbusParser()
    assert parser.can_parse(b"\x01\x03\x14\xAA") is True
    assert parser.can_parse(b"\x99\x03\x14") is False  # Muy corto o ID incorrecto


def test_modbus_parse_valid_data() -> None:
    """Test 2: Valida la extracción precisa de los campos Modbus RTU."""
    parser = ModbusParser()
    result = parser.parse(b"\x01\x03\x19\x55")
    assert result["protocol"] == "Modbus RTU"
    assert result["slave_id"] == 1
    assert result["function_code"] == 3
    assert result["value"] == 25.0


def test_modbus_parse_invalid_raises_error() -> None:
    """Test 3: Comprueba que lance una excepción ante datos corruptos o ajenos."""
    parser = ModbusParser()
    with pytest.raises(ValueError):
        parser.parse(b"\x99\x00\x00")


# --- TESTS NMEA PARSER ---
def test_nmea_can_parse_valid_and_invalid() -> None:
    """Test 4: Verifica la detección de cabeceras de texto GPS."""
    parser = NMEAParser()
    assert parser.can_parse(b"$GPGGA,123456,1929.04,N*4D") is True
    assert parser.can_parse(b"$GPVTG,0,T,,,0,M*33") is False  # Tipo de sentencia errónea


def test_nmea_parse_valid_data() -> None:
    """Test 5: Valida la correcta segmentación de texto y extracción de coordenadas."""
    parser = NMEAParser()
    raw_nmea = b"$GPGGA,123456,19.432,N,96.913,W,1,08"
    result = parser.parse(raw_nmea)
    assert result["protocol"] == "NMEA"
    assert result["latitude"] == "19.432"
    assert result["longitude"] == "96.913"


def test_nmea_parse_invalid_raises_error() -> None:
    """Test 6: Comprueba que rompa adecuadamente si se le pasa una trama binaria aleatoria."""
    parser = NMEAParser()
    with pytest.raises(ValueError):
        parser.parse(b"\x01\x02\x03")