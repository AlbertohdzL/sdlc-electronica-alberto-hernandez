from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.db import Base, engine
from app.routers.alert import router as alert_router
from app.routers.reading import router as reading_router
from app.routers.sensor import router as sensor_router


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None, None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SensorHub Telemetry API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(sensor_router)
app.include_router(reading_router)
app.include_router(alert_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "SensorHub API",
    }