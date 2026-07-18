"""Pruebas unitarias para validar la persistencia con DataRecorder."""

import os
import json
from semana1.uart_driver.recorder import DataRecorder


def test_recorder_initialization() -> None:
    """Test 1: Valida que la ruta del archivo se configure correctamente."""
    recorder = DataRecorder("dummy_path.jsonl")
    assert recorder.filepath == "dummy_path.jsonl"


def test_record_single_entry_writes_jsonl(tmp_path) -> None:
    """Test 2: Verifica que una entrada se transforme en una línea JSON válida."""
    # Creamos un archivo temporal aislado gracias a pytest
    file_path = tmp_path / "telemetry.jsonl"
    recorder = DataRecorder(str(file_path))

    sample_data = {"protocol": "Modbus RTU", "slave_id": 1, "value": 23.5}
    recorder.record(sample_data)

    # Verificamos que el archivo se haya creado físicamente
    assert os.path.exists(file_path)

    # Leemos la línea escrita para comprobar el formato
    with open(file_path, "r", encoding="utf-8") as f:
        line = f.readline()
        parsed_line = json.loads(line)
        
        assert parsed_line["protocol"] == "Modbus RTU"
        assert parsed_line["value"] == 23.5


def test_record_multiple_entries_appends_correctly(tmp_path) -> None:
    """Test 3: Garantiza que múltiples registros se añadan de manera incremental."""
    file_path = tmp_path / "multi_telemetry.jsonl"
    recorder = DataRecorder(str(file_path))

    data_1 = {"id": "sensor_01", "val": 10.0}
    data_2 = {"id": "sensor_02", "val": 20.0}

    recorder.record(data_1)
    recorder.record(data_2)

    # El archivo debe contener exactamente dos líneas escritas
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 2
        assert json.loads(lines[0])["id"] == "sensor_01"
        assert json.loads(lines[1])["id"] == "sensor_02"