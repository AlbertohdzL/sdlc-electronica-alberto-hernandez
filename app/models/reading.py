"""Modelo ORM relacional para Lecturas de Sensores (SQLAlchemy 2.0)."""

from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class ReadingModel(Base):
    """Mapeo de la tabla de lecturas registradas."""

    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(10), nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False
    )