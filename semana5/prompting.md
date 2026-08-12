# Comparativa de Prompting · Semana 5

## Tarea 1: Función Pura de Conversión (`semana5/conversions.py`)

### Prompt Pobre
> Hazme una función para convertir Celsius a Fahrenheit en Python.

**Resultado obtenido:**
Genera una función básica sin type hints, sin validación de límites físicos (cero absoluto) y con explicaciones innecesarias alrededor del código:

def convert(c):
    return (c * 9/5) + 32

### Prompt Bueno
> **CONTEXTO:** API FastAPI (Python 3.12) para gestión de sensores de telemetría.
> **TAREA:** Escribe una función pura `celsius_to_fahrenheit(c: float) -> float` en `semana5/conversions.py`[cite: 1].
> **RESTRICCIONES:** Type hints completos, docstring, redondeo a 2 decimales y lanzar `ValueError` si la temperatura es menor a -273.15 °C[cite: 1].
> **ENTREGA:** Solo la función en código Python, sin explicaciones adicionales[cite: 1].

**Resultado obtenido:**
Código directo, firma tipada correctamente, control explícito de la excepción de física real y listo para producción[cite: 1].
Conversions.py
---

## Tarea 2: Validación de Rangos Físicos con Pydantic v2

### Prompt Pobre
> Crea el esquema de validación para las lecturas de temperatura.

**Resultado obtenido:**
Esquema genérico con `value: float` que acepta temperaturas imposibles (ej. 10,000 °C).

from pydantic import BaseModel

class TemperatureReading(BaseModel):
    sensor_id: str
    value: float

### Prompt Bueno
> **CONTEXTO:** Sistema SensorHub utilizando Pydantic v2.
> **TAREA:** Crea la clase `TemperatureReadingIn` heredando de `BaseModel`.
> **RESTRICCIONES:** Validar que `value` sea float y esté estrictamente entre -50.0 y 150.0 °C usando `Field(ge=..., le=...)`.
> **ENTREGA:** Únicamente el bloque de código con imports.

from pydantic import BaseModel, Field

class TemperatureReadingIn(BaseModel):
    sensor_id: str = Field(..., min_length=1, examples=["TEMP-01"])
    value: float = Field(
        ..., 
        ge=-50.0, 
        le=150.0, 
        description="Temperatura medida en grados Celsius",
        examples=[23.5]
    )
    unit: str = Field("C", pattern="^C$")
---

## Tarea 3: Agregación de Estadísticas de Sensores

### Prompt Pobre
> Haz una función que me dé el promedio de las lecturas.

def promedio(lista):
    return sum(lista) / len(lista)

### Prompt Bueno
> **CONTEXTO:** Capa de servicio de SensorHub para procesamiento en memoria.
> **TAREA:** Escribe la función `calculate_sensor_stats(readings: list[float]) -> dict[str, float]`.
> **RESTRICCIONES:** Retornar diccionario con claves `min`, `max` y `avg` redondeados a 2 decimales. Si la lista está vacía, retornar valores en `0.0`. No usar bibliotecas externas como pandas.
> **ENTREGA:** Código Python estructurado.
def calculate_sensor_stats(readings: list[float]) -> dict[str, float]:
    """
    Calcula el mínimo, máximo y promedio de una lista de lecturas de sensores.

    Si la lista está vacía, retorna 0.0 para todas las métricas para evitar ZeroDivisionError.
    """
    if not readings:
        return {"min": 0.0, "max": 0.0, "avg": 0.0}

    return {
        "min": round(min(readings), 2),
        "max": round(max(readings), 2),
        "avg": round(sum(readings) / len(readings), 2),
    }