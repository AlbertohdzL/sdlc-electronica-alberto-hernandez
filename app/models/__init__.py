"""Módulo de modelos ORM para la base de datos."""

from app.models.alert import AlertModel
from app.models.reading import ReadingModel
from app.models.sensor import SensorModel

__all__ = ["SensorModel", "ReadingModel", "AlertModel"]