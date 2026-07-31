"""Configuración de base de datos y sesiones con SQLAlchemy 2.0."""

import os
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Leemos la URL de la BD desde variable de entorno ( Twelve-Factor App )
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")

# Si es SQLite, deshabilitamos la verificación de hilos para compatibilidad con FastAPI
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Clase base declarativa para los modelos ORM (SQLAlchemy 2.x)."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Inyección de dependencia para obtener una sesión de base de datos limpia por petición."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()