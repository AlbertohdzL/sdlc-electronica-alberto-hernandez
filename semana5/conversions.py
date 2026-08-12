"""Módulo de utilidades de conversión de unidades de telemetría para SensorHub."""


def celsius_to_fahrenheit(c: float) -> float:
    """Convierte grados Celsius a Fahrenheit validando el cero absoluto (-273.15 °C)."""
    if c < -273.15:
        raise ValueError("Temperatura por debajo del cero absoluto (-273.15 °C)")
    return round((c * 9.0 / 5.0) + 32.0, 2)


def fahrenheit_to_celsius(f: float) -> float:
    """Convierte grados Fahrenheit a Celsius validando el cero absoluto (-459.67 °F)."""
    if f < -459.67:
        raise ValueError("Temperatura por debajo del cero absoluto (-459.67 °F)")
    return round((f - 32.0) * 5.0 / 9.0, 2)