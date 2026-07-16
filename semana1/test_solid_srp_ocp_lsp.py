import os
from semana1.solid_srp_ocp_lsp import (
    CalibratedSensor,
    PressureAlert,
    SensorAnalytics,
    SensorData,
    SensorStorage,
    TemperatureAlert,
    ViolacionLSP,
    ViolacionOCP,
    ViolacionSRP,
)


# --- TESTS SRP ---
def test_srp_violacion_saves_correctly(tmp_path) -> None:
    """Test SRP 1: Verifica que la violación funciona pero mezcla tareas."""
    filepath = tmp_path / "bad.json"
    bad_instance = ViolacionSRP("TEMP_01", [20.0, 30.0])
    bad_instance.save_to_file(str(filepath))
    assert os.path.exists(filepath)


def test_srp_correct_implementation(tmp_path) -> None:
    """Test SRP 2: Valida el correcto funcionamiento de las clases segregadas."""
    filepath = tmp_path / "good.json"
    data = SensorData("TEMP_01", [20.0, 30.0])
    analytics = SensorAnalytics()
    storage = SensorStorage()

    avg = analytics.calculate_average(data)
    storage.save_to_json(data, avg, str(filepath))

    assert avg == 25.0
    assert os.path.exists(filepath)


# --- TESTS OCP ---
def test_ocp_violacion() -> None:
    """Test OCP 1: Valida que la clase condicional funciona pero es rígida."""
    v = ViolacionOCP()
    assert v.format_alert("TEMPERATURE", 50.0) == "Alerta Temp: 50.0°C"


def test_ocp_correct_polymorphism() -> None:
    """Test OCP 2: Valida extensiones independientes sin modificar código."""
    temp_alert = TemperatureAlert()
    press_alert = PressureAlert()
    assert temp_alert.format(50.0) == "Alerta Temp: 50.0°C"
    assert press_alert.format(1013.0) == "Alerta Presión: 1013.0 Pa"


# --- TESTS LSP ---
def test_lsp_violacion_breaks_contract() -> None:
    """Test LSP 1: Demuestra cómo la violación rompe la ejecución segura."""
    sensor = ViolacionLSP()
    try:
        sensor.get_voltage()
        assert False, "Debería haber lanzado un error rompiendo el flujo"
    except RuntimeError:
        assert True


def test_lsp_correct_substitution() -> None:
    """Test LSP 2: Comprueba que la subclase sustituye al padre de forma segura."""
    sensor = CalibratedSensor(offset=0.2)
    # Puede ser tratada exactamente igual que la clase base BasicSensor
    assert isinstance(sensor.get_voltage(), float)
    assert sensor.get_voltage() == 3.5