"""Pruebas para el endpoint de verificación de salud (/health)."""

from fastapi.testclient import TestClient


def test_health_check_returns_ok(client: TestClient) -> None:
    """Verifica que /health responda status 200 y el estado sea ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "SensorHub API" in data["service"]