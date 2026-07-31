"""Endpoints REST para la gestión del recurso Reading."""

from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository
from app.schemas.reading import ReadingCreate, ReadingResponse
from app.services.reading_service import ReadingService

router = APIRouter(prefix="/readings", tags=["Readings"])


def get_reading_service(db: Session = Depends(get_db)) -> ReadingService:
    """Inyección de dependencias para el servicio de lecturas."""
    reading_repo = ReadingRepository(db)
    sensor_repo = SensorRepository(db)
    return ReadingService(reading_repo, sensor_repo)


@router.post("", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED)
def create_reading(
    reading_in: ReadingCreate,
    service: ReadingService = Depends(get_reading_service),
) -> ReadingResponse:
    """
    Ingesta una lectura validando:
    - Física real con Pydantic (422 Unprocessable Entity si es inválida).
    - Existencia del sensor en la BD (404 Not Found).
    - Estado activo del sensor (400 Bad Request).
    """
    return service.create_reading(reading_in)


@router.get("/sensor/{sensor_id}", response_model=list[ReadingResponse])
def list_readings_by_sensor(
    sensor_id: str,
    limit: int = Query(50, ge=1, le=100, description="Límite de registros"),
    offset: int = Query(0, ge=0, description="Desplazamiento para paginación"),
    from_date: datetime | None = Query(None, description="Filtro inicio fecha (ISO 8601)"),
    to_date: datetime | None = Query(None, description="Filtro fin fecha (ISO 8601)"),
    service: ReadingService = Depends(get_reading_service),
) -> list[ReadingResponse]:
    """Consulta lecturas con paginación y filtro por rango de fechas (404 si el sensor no existe)."""
    return service.list_readings_by_sensor(
        sensor_id=sensor_id,
        limit=limit,
        offset=offset,
        from_date=from_date,
        to_date=to_date,
    )