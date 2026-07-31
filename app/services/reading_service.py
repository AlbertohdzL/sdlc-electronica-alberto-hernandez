"""Servicio de lógica de negocio para la gestión de lecturas."""

from datetime import datetime
from fastapi import HTTPException, status
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository
from app.schemas.reading import ReadingCreate, ReadingResponse


class ReadingService:
    """Orquesta las reglas de negocio para la ingesta y consulta de lecturas."""

    def __init__(
        self,
        reading_repository: ReadingRepository,
        sensor_repository: SensorRepository,
    ) -> None:
        self.reading_repo = reading_repository
        self.sensor_repo = sensor_repository

    def create_reading(self, reading_in: ReadingCreate) -> ReadingResponse:
        """
        Registra una lectura asegurando que:
        1. El sensor existe en la BD (404 Not Found).
        2. El sensor se encuentra activo (400 Bad Request).
        """
        sensor = self.sensor_repo.get_by_sensor_id(reading_in.sensor_id)
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se puede registrar la lectura. El sensor '{reading_in.sensor_id}' no existe.",
            )

        if not sensor.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El sensor '{reading_in.sensor_id}' está desactivado y no acepta lecturas.",
            )

        db_reading = self.reading_repo.create(reading_in)
        return ReadingResponse.model_validate(db_reading)

    def list_readings_by_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingResponse]:
        """Consulta lecturas con paginación y filtro por fecha previa verificación de existencia del sensor."""
        sensor = self.sensor_repo.get_by_sensor_id(sensor_id)
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El sensor '{sensor_id}' no existe.",
            )

        readings = self.reading_repo.list_by_sensor(
            sensor_id=sensor_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )
        return [ReadingResponse.model_validate(r) for r in readings]