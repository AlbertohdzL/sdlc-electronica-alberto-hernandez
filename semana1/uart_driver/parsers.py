"""Módulo de procesamiento de protocolos (Parsers) para el driver UART."""

from abc import ABC, abstractmethod


class MessageParser(ABC):
    """Clase Base Abstracta que define la interfaz para todos los parsers.

    Aplica OCP al permitir agregar nuevos protocolos sin modificar el dispositivo,
    y LSP al asegurar que cualquier subclase pueda usarse indistintamente.
    """

    @abstractmethod
    def can_parse(self, data: bytes) -> bool:
        """Determina si la trama cruda corresponde a este protocolo específico."""
        pass

    @abstractmethod
    def parse(self, data: bytes) -> dict:
        """Procesa la trama cruda y extrae la información en un diccionario."""
        pass


class ModbusParser(MessageParser):
    """Parser específico para el protocolo binario Modbus RTU."""

    def can_parse(self, data: bytes) -> bool:
        # Modbus RTU es binario. Validamos una longitud mínima de 4 bytes
        # y que empiece con un identificador de esclavo válido (ej. 0x01)
        return len(data) >= 4 and data.startswith(b"\x01")

    def parse(self, data: bytes) -> dict:
        if not self.can_parse(data):
            raise ValueError("La trama no pertenece al protocolo Modbus RTU")

        # Simulación de extracción de bytes: [SlaveID, FunctionCode, DataValue, Checksum]
        return {
            "protocol": "Modbus RTU",
            "slave_id": int(data[0]),
            "function_code": int(data[1]),
            "value": float(data[2]),
        }


class NMEAParser(MessageParser):
    """Parser específico para sentencias de texto NMEA (GPS)."""

    def can_parse(self, data: bytes) -> bool:
        # Las sentencias NMEA son cadenas de texto ASCII que inician con '$GPGGA'
        try:
            text = data.decode("ascii")
            return text.startswith("$GPGGA")
        except UnicodeDecodeError:
            return False

    def parse(self, data: bytes) -> dict:
        if not self.can_parse(data):
            raise ValueError("La trama no pertenece al protocolo NMEA")

        text = data.decode("ascii")
        parts = text.split(",")

        # Formato esperado: $GPGGA,timestamp,latitud,N,longitud,W,...
        # Extraemos latitud y longitud protegiendo índices
        latitude = parts[2] if len(parts) > 2 else "0.0"
        longitude = parts[4] if len(parts) > 4 else "0.0"

        return {
            "protocol": "NMEA",
            "sentence_type": "GPGGA",
            "latitude": latitude,
            "longitude": longitude,
        }