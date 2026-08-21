from app.models.alert import AlertModel
from app.repositories.alert_repository import AlertRepository


class AlertService:
    VALID_STATUSES = {"open", "acknowledged", "resolved"}

    def __init__(self, repo: AlertRepository) -> None:
        self._repo = repo

    def list_alerts(self, status: str | None = None) -> list[AlertModel]:
        return self._repo.list_alerts(status=status)

    def update_status(self, alert_id: int, new_status: str) -> AlertModel:
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Estado '{new_status}' no válido. Opciones: {self.VALID_STATUSES}")
        
        alert = self._repo.update_status(alert_id, new_status)
        if alert is None:
            raise LookupError(f"Alerta con ID {alert_id} no encontrada")
        return alert