from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.alert import AlertModel


def test_list_alerts_empty(client: TestClient) -> None:
    """Verifica que el listado de alertas inicie vacío."""
    response = client.get("/alerts")
    assert response.status_code == 200
    assert response.json() == []


def test_alert_lifecycle_and_filtering(client: TestClient, db_session: Session) -> None:
    """Prueba el ciclo de vida de una alerta (open -> acknowledged -> resolved) y filtros."""
    # 1. Crear alerta de prueba en BD
    alert = AlertModel(
        sensor_id=1,
        reading_id=1,
        value=42.5,
        threshold=35.0,
        status="open",
    )
    db_session.add(alert)
    db_session.commit()
    db_session.refresh(alert)

    # 2. Consultar lista
    res_list = client.get("/alerts?status=open")
    assert res_list.status_code == 200
    assert len(res_list.json()) == 1

    # 3. Transicionar a acknowledged
    res_ack = client.patch(f"/alerts/{alert.id}", json={"status": "acknowledged"})
    assert res_ack.status_code == 200
    assert res_ack.json()["status"] == "acknowledged"

    # 4. Transicionar a resolved
    res_res = client.patch(f"/alerts/{alert.id}", json={"status": "resolved"})
    assert res_res.status_code == 200
    assert res_res.json()["status"] == "resolved"


def test_update_alert_invalid_status_422(client: TestClient, db_session: Session) -> None:
    """Verifica que un estado no permitido retorne 422."""
    alert = AlertModel(sensor_id=1, reading_id=1, value=50.0, threshold=30.0, status="open")
    db_session.add(alert)
    db_session.commit()
    db_session.refresh(alert)

    response = client.patch(f"/alerts/{alert.id}", json={"status": "invalido"})
    assert response.status_code == 422


def test_update_non_existent_alert_404(client: TestClient) -> None:
    """Verifica que actualizar una alerta inexistente retorne 404."""
    response = client.patch("/alerts/9999", json={"status": "resolved"})
    assert response.status_code == 404