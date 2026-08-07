"""Punto de entrada principal de la aplicación FastAPI (SensorHub)."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import Base, engine
from app.routers import reading_router, sensor_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Crea las tablas en la base de datos relacional al iniciar la aplicación."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SensorHub API",
    description="API REST modular en 4 capas para monitoreo IoT de sensores industriales.",
    version="1.0.0",
    lifespan=lifespan,
)

# Registro de routers
app.include_router(sensor_router)
app.include_router(reading_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Endpoint de verificación de salud del servicio."""
    return {"status": "ok", "service": "SensorHub API"}
@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    """Endpoint raíz para verificación de salud de Render."""
    return {"message": "Bienvenido a SensorHub API", "docs": "/docs"}