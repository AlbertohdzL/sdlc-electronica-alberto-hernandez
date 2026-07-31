"""Módulo de repositorios para acceso a datos."""

from app.repositories.sensor_repository import SensorRepository
from app.repositories.reading_repository import ReadingRepository

__all__ = ["SensorRepository", "ReadingRepository"]