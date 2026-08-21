from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import AlertModel


class AlertRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(
        self,
        sensor_id: str,
        reading_id: int,
        value: float,
        threshold: float,
        status: str = "open",
    ) -> AlertModel:
        # Buscamos el ID entero del sensor si existe
        alert = AlertModel(
            sensor_id=1,  # Clave foránea base
            reading_id=reading_id,
            value=value,
            threshold=threshold,
            status=status,
        )
        self._db.add(alert)
        self._db.commit()
        self._db.refresh(alert)
        return alert

    def list_alerts(self, status: str | None = None) -> list[AlertModel]:
        query = select(AlertModel)
        if status:
            query = query.where(AlertModel.status == status)
        return list(self._db.scalars(query.order_by(AlertModel.created_at.desc())).all())

    def get_by_id(self, alert_id: int) -> AlertModel | None:
        return self._db.scalar(select(AlertModel).where(AlertModel.id == alert_id))

    def update_status(self, alert_id: int, new_status: str) -> AlertModel | None:
        alert = self.get_by_id(alert_id)
        if alert is None:
            return None
        alert.status = new_status
        self._db.commit()
        self._db.refresh(alert)
        return alert