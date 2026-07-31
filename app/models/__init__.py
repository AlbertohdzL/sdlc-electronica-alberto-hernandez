"""Módulo de modelos ORM para la base de datos."""

from app.models.sensor import SensorModel
from app.models.reading import ReadingModel

__all__ = ["SensorModel", "ReadingModel"]