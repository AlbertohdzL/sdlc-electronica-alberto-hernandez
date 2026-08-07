"""Pruebas de integración para los endpoints de Lecturas (/readings)."""

from fastapi.testclient import TestClient


def test_create_reading_success(client: TestClient) -> None:
    """Prueba el registro exitoso de una lectura válida."""
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "location": "Bodega A", "sensor_type": "temperature", "alert_threshold": 35.0},
    )

    payload = {
        "sensor_id": "TEMP-01",
        "value": 24.5,
        "unit": "C",
        "sensor_type": "temperature",
    }
    response = client.post("/readings", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["value"] == 24.5
    assert "created_at" in data


def test_create_reading_invalid_physical_value_422(client: TestClient) -> None:
    """Prueba el rechazo de Pydantic por valor fuera de rango físico (422 Unprocessable Entity)."""
    payload = {
        "sensor_id": "TEMP-01",
        "value": -300.0,  # Bajo el cero absoluto
        "unit": "C",
        "sensor_type": "temperature",
    }
    response = client.post("/readings", json=payload)
    assert response.status_code == 422


def test_create_reading_non_existent_sensor_404(client: TestClient) -> None:
    """Prueba que registrar lectura a un sensor que no existe retorne 404 Not Found."""
    payload = {
        "sensor_id": "GHOST-99",
        "value": 25.0,
        "unit": "C",
        "sensor_type": "temperature",
    }
    response = client.post("/readings", json=payload)
    assert response.status_code == 404


def test_create_reading_deactivated_sensor_400(client: TestClient) -> None:
    """Prueba que registrar lectura en un sensor desactivado retorne 400 Bad Request."""
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-OFF", "location": "Bodega B", "sensor_type": "temperature", "alert_threshold": 35.0},
    )
    client.delete("/sensors/TEMP-OFF")

    payload = {
        "sensor_id": "TEMP-OFF",
        "value": 22.0,
        "unit": "C",
        "sensor_type": "temperature",
    }
    response = client.post("/readings", json=payload)
    assert response.status_code == 400
    assert "está desactivado" in response.json()["detail"]


def test_list_readings_by_sensor_success(client: TestClient) -> None:
    """Prueba la consulta de historial de lecturas por sensor."""
    client.post(
        "/sensors",
        json={"sensor_id": "HUM-01", "location": "Pasillo C", "sensor_type": "humidity", "alert_threshold": 80.0},
    )
    client.post("/readings", json={"sensor_id": "HUM-01", "value": 55.0, "unit": "%", "sensor_type": "humidity"})

    response = client.get("/readings/sensor/HUM-01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["value"] == 55.0