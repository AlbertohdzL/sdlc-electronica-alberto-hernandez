"""Pruebas de integración para los endpoints de Sensores (/sensors)."""

from fastapi.testclient import TestClient


def test_create_sensor_success(client: TestClient) -> None:
    """Prueba la creación exitosa de un sensor (201 Created)."""
    payload = {
        "sensor_id": "TEMP-10",
        "location": "Nave Industrial 1",
        "sensor_type": "temperature",
        "alert_threshold": 35.0,
    }
    response = client.post("/sensors", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["sensor_id"] == "TEMP-10"
    assert data["is_active"] is True
    assert "id" in data


def test_create_duplicate_sensor_conflict(client: TestClient) -> None:
    """Prueba que registrar un sensor_id existente devuelva 409 Conflict."""
    payload = {
        "sensor_id": "TEMP-10",
        "location": "Nave Industrial 1",
        "sensor_type": "temperature",
        "alert_threshold": 35.0,
    }
    client.post("/sensors", json=payload)
    response = client.post("/sensors", json=payload)
    assert response.status_code == 409
    assert "ya está registrado" in response.json()["detail"]


def test_get_sensor_by_id_success(client: TestClient) -> None:
    """Prueba la consulta de un sensor por su ID."""
    payload = {
        "sensor_id": "HUM-01",
        "location": "Pasillo B",
        "sensor_type": "humidity",
        "alert_threshold": 80.0,
    }
    client.post("/sensors", json=payload)

    response = client.get("/sensors/HUM-01")
    assert response.status_code == 200
    assert response.json()["location"] == "Pasillo B"


def test_get_non_existent_sensor_404(client: TestClient) -> None:
    """Prueba la consulta de un sensor inexistente (404 Not Found)."""
    response = client.get("/sensors/GHOST-99")
    assert response.status_code == 404


def test_list_sensors_paginated(client: TestClient) -> None:
    """Prueba el listado paginado de sensores."""
    client.post(
        "/sensors",
        json={"sensor_id": "S-1", "location": "L1", "sensor_type": "temperature", "alert_threshold": 30.0},
    )
    client.post(
        "/sensors",
        json={"sensor_id": "S-2", "location": "L2", "sensor_type": "humidity", "alert_threshold": 70.0},
    )

    response = client.get("/sensors?limit=1&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["sensor_id"] == "S-1"


def test_deactivate_sensor_success(client: TestClient) -> None:
    """Prueba la desactivación suave de un sensor."""
    client.post(
        "/sensors",
        json={"sensor_id": "S-OFF", "location": "L3", "sensor_type": "temperature", "alert_threshold": 40.0},
    )

    response = client.delete("/sensors/S-OFF")
    assert response.status_code == 200
    assert response.json()["is_active"] is False