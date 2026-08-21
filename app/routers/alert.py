from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert import AlertOut, AlertUpdate
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])


def get_alert_service(db: Session = Depends(get_db)) -> AlertService:
    return AlertService(AlertRepository(db))


@router.get("", response_model=list[AlertOut])
def list_alerts(
    status: str | None = None,
    service: AlertService = Depends(get_alert_service),
) -> list[AlertOut]:
    """GET /alerts — Lista alertas registradas con filtro opcional por estado."""
    alerts = service.list_alerts(status=status)
    return [AlertOut.model_validate(a) for a in alerts]


@router.patch("/{alert_id}", response_model=AlertOut)
def update_alert_status(
    alert_id: int,
    payload: AlertUpdate,
    service: AlertService = Depends(get_alert_service),
) -> AlertOut:
    """PATCH /alerts/{id} — Transiciona el ciclo de vida de la alerta."""
    try:
        updated = service.update_status(alert_id, payload.status)
        return AlertOut.model_validate(updated)
    except ValueError as err:
        raise HTTPException(status_code=422, detail=str(err)) from err
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err