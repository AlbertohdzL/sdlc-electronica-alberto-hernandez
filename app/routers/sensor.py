from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.reading import ReadingModel
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor import SensorCreate, SensorResponse, SensorStats, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["sensors"])


def get_sensor_service(db: Session = Depends(get_db)) -> SensorService:
    return SensorService(SensorRepository(db))


@router.post("", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def create_sensor(
    sensor_in: SensorCreate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    try:
        return service.create_sensor(sensor_in)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[SensorResponse])
def list_sensors(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SensorService = Depends(get_sensor_service),
) -> list[SensorResponse]:
    return service.list_sensors(limit=limit, offset=offset)


@router.get("/{sensor_id}/stats", response_model=SensorStats)
def get_sensor_statistics(
    sensor_id: str,
    db: Session = Depends(get_db),
    service: SensorService = Depends(get_sensor_service),
) -> SensorStats:
    """GET /sensors/{id}/stats — Retorna min, max, avg y conteo de lecturas."""
    sensor = service.get_sensor(sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} no encontrado")

    stmt = select(
        func.count(ReadingModel.id),
        func.min(ReadingModel.value),
        func.max(ReadingModel.value),
        func.avg(ReadingModel.value),
    ).where(ReadingModel.sensor_id == sensor_id)

    row = db.execute(stmt).one()
    count: int = row[0] or 0
    min_val: float | None = float(row[1]) if row[1] is not None else None
    max_val: float | None = float(row[2]) if row[2] is not None else None
    avg_val: float | None = round(float(row[3]), 2) if row[3] is not None else None

    return SensorStats(
        sensor_id=sensor_id,
        count=count,
        min_value=min_val,
        max_value=max_val,
        avg_value=avg_val,
    )


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(
    sensor_id: str,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    sensor = service.get_sensor(sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} no encontrado")
    return sensor


@router.patch("/{sensor_id}", response_model=SensorResponse)
def update_sensor(
    sensor_id: str,
    sensor_in: SensorUpdate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    updated = service.update_sensor(sensor_id, sensor_in)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} no encontrado")
    return updated


@router.delete("/{sensor_id}", response_model=SensorResponse)
def deactivate_sensor(
    sensor_id: str,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    res = service.deactivate_sensor(sensor_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} no encontrado")

    sensor = service.get_sensor(sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} no encontrado")
    return sensor