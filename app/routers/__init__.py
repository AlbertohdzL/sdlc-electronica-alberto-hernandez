"""Módulo de routers de la API."""

from app.routers.sensor import router as sensor_router
from app.routers.reading import router as reading_router

__all__ = ["sensor_router", "reading_router"]