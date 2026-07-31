"""Modelo ORM relacional para Sensores (SQLAlchemy 2.0)."""

from datetime import datetime, timezone
from sqlalchemy import String, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class SensorModel(Base):
    """Mapeo de la tabla de sensores en la base de datos."""

    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(20), nullable=False)
    alert_threshold: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )