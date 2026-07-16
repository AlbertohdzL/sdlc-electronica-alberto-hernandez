"""Módulo que ejemplifica los principios SOLID: ISP y DIP.

Utiliza Protocols de Python para segregar interfaces y aplicar la inyección
de dependencias en arquitecturas de adquisición de datos.
"""

from typing import Protocol

# =====================================================================
# 4. INTERFACE SEGREGATION PRINCIPLE (ISP)
# =====================================================================

# MAL: Interfaz gorda. Obliga a sensores de solo lectura a implementar escritura.
class ViolacionISP(Protocol):
    def read_data(self) -> float: ...
    def write_data(self, data: float) -> None: ...  # Innecesario para sensores puros


# BIEN: Interfaces segregadas y especializadas.
class ReaderProtocol(Protocol):
    """Interfaz enfocada exclusivamente en operaciones de lectura."""
    def read_data(self) -> float: ...


class WriterProtocol(Protocol):
    """Interfaz enfocada exclusivamente en operaciones de escritura."""
    def write_data(self, data: float) -> None: ...


class OnlyReaderSensor:
    """Implementa únicamente la interfaz de lectura sin acoplamientos inútiles."""
    def __init__(self, fixed_value: float) -> None:
        self.fixed_value = fixed_value

    def read_data(self) -> float:
        return self.fixed_value


# =====================================================================
# 5. DEPENDENCY INVERSION PRINCIPLE (DIP)
# =====================================================================

class HardcodedHardware:
    """Módulo de bajo nivel (Driver de un sensor específico)."""
    def read_raw_voltage(self) -> float:
        return 1.8


# MAL: Clase de alto nivel acoplada rígidamente al driver de bajo nivel.
class ViolacionDIP:
    def __init__(self) -> None:
        # Dependencia directa de la implementación concreta
        self.sensor = HardcodedHardware()

    def get_percentage(self) -> float:
        # Si cambia el método o el chip, esta clase se rompe
        return (self.sensor.read_raw_voltage() / 3.3) * 100


# BIEN: La clase de alto nivel depende de una abstracción (ReaderProtocol).
class DataProcessor:
    """Módulo de alto nivel desacoplado por inversión de dependencias."""

    def __init__(self, datasource: ReaderProtocol) -> None:
        # Inyección de dependencias vía interfaz/protocolo
        self.datasource = datasource

    def get_percentage(self) -> float:
        return (self.datasource.read_data() / 3.3) * 100