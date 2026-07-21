"""Pruebas unitarias para AlertManager y sus estrategias (TDD - US-03)."""

from semana2.eval1.alert_manager import (
    AlertManager,
    ConsoleAlertStrategy,
    FileAlertStrategy,
)


def test_console_alert_strategy_prints_message(capsys) -> None:
    """Escenario Gherkin 1: Emisión de alerta por consola."""
    strategy = ConsoleAlertStrategy()
    manager = AlertManager(strategy)
    manager.notify("ALERTA: Temperatura crítica en TEMP-02")

    captured = capsys.readouterr()
    assert "ALERTA: Temperatura crítica en TEMP-02" in captured.out


def test_file_alert_strategy_writes_to_file(tmp_path) -> None:
    """Escenario Gherkin 2: Emisión de alerta formateada en archivo log."""
    log_file = tmp_path / "alerts.log"
    strategy = FileAlertStrategy(str(log_file))
    manager = AlertManager(strategy)
    manager.notify("ALERTA: Humedad alta en HUM-03")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "ALERTA: Humedad alta en HUM-03" in content