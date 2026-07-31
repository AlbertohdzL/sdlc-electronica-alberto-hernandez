"""Repositorio para el acceso a datos del recurso Sensor."""

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.sensor import SensorModel
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorRepository:
    """Maneja las operaciones de persistencia en la tabla sensors."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, sensor_in: SensorCreate) -> SensorModel:
        """Persiste un nuevo sensor en la base de datos."""
        db_sensor = SensorModel(
            sensor_id=sensor_in.sensor_id,
            location=sensor_in.location,
            sensor_type=sensor_in.sensor_type,
            alert_threshold=sensor_in.alert_threshold,
            is_active=True,
        )
        self.db.add(db_sensor)
        self.db.commit()
        self.db.refresh(db_sensor)
        return db_sensor

    def get_by_sensor_id(self, sensor_id: str) -> SensorModel | None:
        """Busca un sensor único por su identificador de texto (ej. TEMP-01)."""
        stmt = select(SensorModel).where(SensorModel.sensor_id == sensor_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        """Consulta sensores registrados con paginación."""
        stmt = select(SensorModel).offset(offset).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def update(self, db_sensor: SensorModel, sensor_in: SensorUpdate) -> SensorModel:
        """Actualiza campos específicos de un sensor."""
        update_data = sensor_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sensor, field, value)
        self.db.commit()
        self.db.refresh(db_sensor)
        return db_sensor

    def deactivate(self, db_sensor: SensorModel) -> SensorModel:
        """Desactiva un sensor (soft delete) cumpliendo reglas de producción."""
        db_sensor.is_active = False
        self.db.commit()
        self.db.refresh(db_sensor)
        return db_sensor