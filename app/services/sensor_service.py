"""Servicio de lógica de negocio para la gestión de sensores."""

from fastapi import HTTPException, status
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate


class SensorService:
    """Orquesta las reglas de negocio y validaciones del recurso Sensor."""

    def __init__(self, repository: SensorRepository) -> None:
        self.repository = repository

    def create_sensor(self, sensor_in: SensorCreate) -> SensorResponse:
        """Crea un sensor verificando que el sensor_id no exista previamente (409 Conflict)."""
        existing = self.repository.get_by_sensor_id(sensor_in.sensor_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El sensor con ID '{sensor_in.sensor_id}' ya está registrado.",
            )
        db_sensor = self.repository.create(sensor_in)
        return SensorResponse.model_validate(db_sensor)

    def get_sensor(self, sensor_id: str) -> SensorResponse:
        """Obtiene las propiedades de un sensor o lanza 404 Not Found."""
        db_sensor = self.repository.get_by_sensor_id(sensor_id)
        if not db_sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El sensor '{sensor_id}' no fue encontrado.",
            )
        return SensorResponse.model_validate(db_sensor)

    def list_sensors(self, limit: int = 50, offset: int = 0) -> list[SensorResponse]:
        """Obtiene la lista paginada de sensores."""
        sensors = self.repository.list_all(limit=limit, offset=offset)
        return [SensorResponse.model_validate(s) for s in sensors]

    def update_sensor(self, sensor_id: str, sensor_in: SensorUpdate) -> SensorResponse:
        """Actualiza un sensor existente o lanza 404 Not Found."""
        db_sensor = self.repository.get_by_sensor_id(sensor_id)
        if not db_sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El sensor '{sensor_id}' no existe.",
            )
        updated = self.repository.update(db_sensor, sensor_in)
        return SensorResponse.model_validate(updated)

    def deactivate_sensor(self, sensor_id: str) -> SensorResponse:
        """Desactiva un sensor (soft delete) o lanza 404 Not Found."""
        db_sensor = self.repository.get_by_sensor_id(sensor_id)
        if not db_sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El sensor '{sensor_id}' no existe.",
            )
        deactivated = self.repository.deactivate(db_sensor)
        return SensorResponse.model_validate(deactivated)