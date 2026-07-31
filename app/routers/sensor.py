"""Endpoints REST para la gestión del recurso Sensor."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])


def get_sensor_service(db: Session = Depends(get_db)) -> SensorService:
    """Inyección de dependencias para el servicio de sensores."""
    repository = SensorRepository(db)
    return SensorService(repository)


@router.post("", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def create_sensor(
    sensor_in: SensorCreate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    """Registra un nuevo sensor (retorna 409 Conflict si el ID ya existe)."""
    return service.create_sensor(sensor_in)


@router.get("", response_model=list[SensorResponse])
def list_sensors(
    limit: int = Query(50, ge=1, le=100, description="Límite de registros"),
    offset: int = Query(0, ge=0, description="Desplazamiento para paginación"),
    service: SensorService = Depends(get_sensor_service),
) -> list[SensorResponse]:
    """Consulta la lista de sensores registrados con paginación."""
    return service.list_sensors(limit=limit, offset=offset)


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(
    sensor_id: str,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    """Obtiene los detalles de un sensor por su ID de texto (404 si no existe)."""
    return service.get_sensor(sensor_id)


@router.patch("/{sensor_id}", response_model=SensorResponse)
def update_sensor(
    sensor_id: str,
    sensor_in: SensorUpdate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    """Actualiza parcialmente un sensor (404 si no existe)."""
    return service.update_sensor(sensor_id, sensor_in)


@router.delete("/{sensor_id}", response_model=SensorResponse)
def deactivate_sensor(
    sensor_id: str,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    """Desactiva un sensor (soft delete en producción, 404 si no existe)."""
    return service.deactivate_sensor(sensor_id)