from fastapi.testclient import TestClient


def test_get_sensor_stats_success(client: TestClient) -> None:
    """Prueba el cálculo de métricas agregadas (min, max, avg, count)."""
    # 1. Crear sensor
    client.post(
        "/sensors",
        json={"sensor_id": "STAT-01", "location": "Zona A", "sensor_type": "temperature"},
    )

    # 2. Registrar lecturas
    client.post("/readings", json={"sensor_id": "STAT-01", "value": 10.0, "unit": "C", "sensor_type": "temperature"})
    client.post("/readings", json={"sensor_id": "STAT-01", "value": 20.0, "unit": "C", "sensor_type": "temperature"})
    client.post("/readings", json={"sensor_id": "STAT-01", "value": 30.0, "unit": "C", "sensor_type": "temperature"})

    # 3. Consultar estadísticas
    response = client.get("/sensors/STAT-01/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["sensor_id"] == "STAT-01"
    assert data["count"] == 3
    assert data["min_value"] == 10.0
    assert data["max_value"] == 30.0
    assert data["avg_value"] == 20.0


def test_get_sensor_stats_non_existent_sensor_404(client: TestClient) -> None:
    """Verifica que consultar estadísticas de un sensor inexistente retorne 404."""
    response = client.get("/sensors/NO-EXISTE/stats")
    assert response.status_code == 404