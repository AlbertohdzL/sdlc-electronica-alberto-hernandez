"""Repositorio para el acceso a datos del recurso Reading con paginación y filtros."""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.reading import ReadingModel
from app.schemas.reading import ReadingCreate


class ReadingRepository:
    """Maneja las operaciones de persistencia de lecturas de sensores."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, reading_in: ReadingCreate) -> ReadingModel:
        """Persiste una lectura en la base de datos."""
        db_reading = ReadingModel(
            sensor_id=reading_in.sensor_id,
            value=reading_in.value,
            unit=reading_in.unit,
            sensor_type=reading_in.sensor_type,
        )
        self.db.add(db_reading)
        self.db.commit()
        self.db.refresh(db_reading)
        return db_reading

    def list_by_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingModel]:
        """Consulta el historial de lecturas con paginación y filtro por rango de fechas."""
        stmt = select(ReadingModel).where(ReadingModel.sensor_id == sensor_id)

        if from_date:
            stmt = stmt.where(ReadingModel.created_at >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.created_at <= to_date)

        stmt = stmt.order_by(ReadingModel.created_at.desc()).offset(offset).limit(limit)
        return list(self.db.execute(stmt).scalars().all())