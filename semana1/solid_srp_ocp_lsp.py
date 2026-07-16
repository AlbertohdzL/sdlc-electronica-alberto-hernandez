"""Módulo que ejemplifica los principios SOLID: SRP, OCP y LSP."""

import json
from typing import List


# =====================================================================
# 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# =====================================================================

# MAL: La clase maneja datos, lógica de negocio y persistencia en disco.
class ViolacionSRP:

    def __init__(self, sensor_id: str, readings: List[float]) -> None:
        self.sensor_id = sensor_id
        self.readings = readings

    def calculate_average(self) -> float:
        return sum(self.readings) / len(self.readings) if self.readings else 0.0

    def save_to_file(self, filename: str) -> None:
        data = {"id": self.sensor_id, "avg": self.calculate_average()}
        with open(filename, "w") as f:
            json.dump(data, f)


# BIEN: Separación total de responsabilidades.
class SensorData:
    """Única responsabilidad: Almacenar los datos del sensor."""

    def __init__(self, sensor_id: str, readings: List[float]) -> None:
        self.sensor_id = sensor_id
        self.readings = readings


class SensorAnalytics:
    """Única responsabilidad: Procesamiento matemático y cálculos."""

    def calculate_average(self, sensor: SensorData) -> float:
        return (
            sum(sensor.readings) / len(sensor.readings)
            if sensor.readings
            else 0.0
        )


class SensorStorage:
    """Única responsabilidad: Operaciones de entrada/salida (I/O)."""

    def save_to_json(
        self, sensor: SensorData, average: float, filename: str
    ) -> None:
        data = {"id": sensor.sensor_id, "avg": average}
        with open(filename, "w") as f:
            json.dump(data, f)


# =====================================================================
# 2. OPEN/CLOSED PRINCIPLE (OCP)
# =====================================================================

# MAL: Si agregamos un nuevo tipo de sensor, hay que modificar esta clase
# agregando más bloques condicionales (if-elif).
class ViolacionOCP:

    def format_alert(self, sensor_type: str, value: float) -> str:
        if sensor_type == "TEMPERATURE":
            return f"Alerta Temp: {value}°C"
        elif sensor_type == "PRESSURE":
            return f"Alerta Presión: {value} Pa"
        return f"Alerta Genérica: {value}"


# BIEN: Abierto a la extensión, cerrado a la modificación mediante polimorfismo.
class AlertFormatter:
    """Clase base para formatear alertas (Cerrada a modificaciones)."""

    def format(self, value: float) -> str:
        return f"Alerta Genérica: {value}"


class TemperatureAlert(AlertFormatter):
    """Extensión para temperatura sin modificar la clase base."""

    def format(self, value: float) -> str:
        return f"Alerta Temp: {value}°C"


class PressureAlert(AlertFormatter):
    """Extensión para presión sin modificar la clase base."""

    def format(self, value: float) -> str:
        return f"Alerta Presión: {value} Pa"


# =====================================================================
# 3. LISKOV SUBSTITUTION PRINCIPLE (LSP)
# =====================================================================

class BasicSensor:

    def get_voltage(self) -> float:
        return 3.3


# MAL: Rompe el principio porque cambia el tipo de retorno esperado (str)
# o lanza excepciones imprevistas que rompen el flujo del programa principal.
class ViolacionLSP(BasicSensor):

    def get_voltage(self) -> float:
        # Rompe el contrato al no devolver un float válido
        raise RuntimeError("Error de Hardware simulado")


# BIEN: La subclase extiende el comportamiento pero respeta al 100% el contrato.
class CalibratedSensor(BasicSensor):

    def __init__(self, offset: float) -> None:
        self.offset = offset

    def get_voltage(self) -> float:
        # Retorna el tipo float esperado, manteniendo la estabilidad del sistema
        return super().get_voltage() + self.offset