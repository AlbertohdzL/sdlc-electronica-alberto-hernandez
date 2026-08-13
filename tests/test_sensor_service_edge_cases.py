from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException

from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.services.sensor_service import SensorService


@pytest.fixture
def mock_repo():
    """Crea un repositorio simulado (Mock) aislado de la base de datos."""
    return MagicMock(spec=SensorRepository)


@pytest.fixture
def service(mock_repo):
    """Instancia el servicio inyectándole el repositorio simulado."""
    return SensorService(repository=mock_repo)


def test_edge_case_1_create_sensor_already_exists(service, mock_repo):
    """Test 1: Intentar crear un sensor que ya existe lanza HTTPException 409 Conflict."""
    mock_repo.get_by_sensor_id.return_value = MagicMock(id=1, sensor_id="TEMP-01")
    sensor_in = SensorCreate(
    sensor_id="TEMP-01",
    sensor_type="temperature",
    location="Lab 1",
    alert_threshold=35.0,
)

    with pytest.raises(HTTPException) as exc_info:
        service.create_sensor(sensor_in)

    assert exc_info.value.status_code == 409
    assert "ya está registrado" in exc_info.value.detail


def test_edge_case_2_get_sensor_not_found(service, mock_repo):
    """Test 2: Consultar un sensor inexistente lanza HTTPException 404 Not Found."""
    mock_repo.get_by_sensor_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.get_sensor("GHOST-99")

    assert exc_info.value.status_code == 404
    assert "no fue encontrado" in exc_info.value.detail


def test_edge_case_3_update_sensor_not_found(service, mock_repo):
    """Test 3: Intentar actualizar un sensor inexistente lanza HTTPException 404 Not Found."""
    mock_repo.get_by_sensor_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.update_sensor("GHOST-99", SensorUpdate(location="Nueva Sala"))

    assert exc_info.value.status_code == 404


def test_edge_case_4_deactivate_sensor_not_found(service, mock_repo):
    """Test 4: Intentar desactivar un sensor inexistente lanza HTTPException 404 Not Found."""
    mock_repo.get_by_sensor_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.deactivate_sensor("GHOST-99")

    assert exc_info.value.status_code == 404


def test_edge_case_5_list_sensors_empty_repository(service, mock_repo):
    """Test 5: Listar sensores cuando el repositorio está vacío retorna una lista vacía."""
    mock_repo.list_all.return_value = []

    result = service.list_sensors(limit=10, offset=0)

    assert result == []
    mock_repo.list_all.assert_called_once_with(limit=10, offset=0)