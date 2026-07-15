"""Módulo de procesamiento idiomático de lecturas de sensores.

Este módulo implementa el modelado de datos inmutables y funciones puras
para el procesamiento de telemetría, reemplazando las estructuras mutables de C.
"""

from dataclasses import dataclass, replace
from enum import Enum, auto
from typing import Protocol


class SensorType(Enum):
    """Tipos de sensores soportados por la arquitectura."""

    TEMPERATURE = auto()
    PRESSURE = auto()
    HUMIDITY = auto()


class SensorStatus(Enum):
    """Estados operacionales del sensor basados en umbrales."""

    OK = auto()
    WARN = auto()
    CRITICAL = auto()


@dataclass(frozen=True)
class Reading:
    """Representación inmutable de la lectura de un hardware.

    Equivalente a una captura limpia de un registro de sensor.
    Al ser 'frozen=True', se garantiza la inmutabilidad de los datos.
    """

    sensor_id: str
    sensor_type: SensorType
    value: float
    timestamp: float
    status: SensorStatus = SensorStatus.OK


class Processor(Protocol):
    """Protocolo estructural para procesamiento de lecturas.

    Define la interfaz esperada mediante Duck Typing, eliminando la necesidad
    de usar punteros a funciones explícitos al estilo de C.
    """

    def process(self, reading: Reading) -> Reading:
        """Procesa una lectura y retorna una nueva instancia modificada."""
        ...


# ==========================================
# 5 FUNCIONES PURAS DE PROCESAMIENTO
# ==========================================

def celsius_to_fahrenheit(reading: Reading) -> Reading:
    """Función Pura 1: Convierte la unidad si el sensor es de temperatura.

    No altera la instancia original; retorna una nueva copia modificada.
    """
    if reading.sensor_type != SensorType.TEMPERATURE:
        return reading

    converted_value = (reading.value * 9 / 5) + 32
    return replace(reading, value=converted_value)


def is_out_of_bounds(reading: Reading, min_val: float, max_val: float) -> bool:
    """Función Pura 2: Predicado que evalúa seguridad física del entorno."""
    return reading.value < min_val or reading.value > max_val


def apply_calibration_offset(reading: Reading, offset: float) -> Reading:
    """Función Pura 3: Aplica un offset de calibración de hardware."""
    calibrated_value = reading.value + offset
    return replace(reading, value=calibrated_value)


def update_reading_status(
    reading: Reading, low_threshold: float, high_threshold: float
) -> Reading:
    """Función Pura 4: Evalúa límites y actualiza el estado operacional."""
    if reading.value > high_threshold:
        new_status = SensorStatus.CRITICAL
    elif reading.value < low_threshold:
        new_status = SensorStatus.WARN
    else:
        new_status = SensorStatus.OK

    return replace(reading, status=new_status)


def to_telemetry_string(reading: Reading) -> str:
    """Función Pura 5: Serializa a cadena de texto para transmisión UART/Red."""
    return (
        f"[{reading.timestamp:.2f}] ID:{reading.sensor_id} | "
        f"TYPE:{reading.sensor_type.name} | VAL:{reading.value:.2f} | "
        f"STATUS:{reading.status.name}"
    )

