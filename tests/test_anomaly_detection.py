from unittest.mock import MagicMock
import pytest
from app.services.anomaly_detector import (
    AlertStrategy,
    AnomalyDetector,
    ConsoleAlertStrategy,
    InMemoryAlertStrategy,
)


def test_no_anomaly_when_value_below_threshold():
    """No debe disparar alertas si el valor está por debajo del umbral."""
    mock_strategy = MagicMock(spec=AlertStrategy)
    detector = AnomalyDetector(strategy=mock_strategy)

    triggered = detector.evaluate(sensor_id="TEMP-01", value=28.5, threshold=35.0)

    assert triggered is False
    mock_strategy.send_alert.assert_not_called()


def test_anomaly_triggers_alert_when_value_exceeds_threshold():
    """Debe disparar una alerta cuando el valor supera el umbral configurado."""
    mock_strategy = MagicMock(spec=AlertStrategy)
    detector = AnomalyDetector(strategy=mock_strategy)

    triggered = detector.evaluate(sensor_id="TEMP-01", value=42.0, threshold=35.0)

    assert triggered is True
    mock_strategy.send_alert.assert_called_once()
    args, kwargs = mock_strategy.send_alert.call_args
    assert "TEMP-01" in args[0]
    assert "42.0" in args[0]


def test_in_memory_alert_strategy_stores_alerts():
    """La estrategia en memoria debe almacenar el historial de alertas emitidas (OCP)."""
    strategy = InMemoryAlertStrategy()
    detector = AnomalyDetector(strategy=strategy)

    detector.evaluate(sensor_id="TEMP-01", value=38.0, threshold=30.0)
    detector.evaluate(sensor_id="TEMP-02", value=95.0, threshold=80.0)

    assert len(strategy.alerts) == 2
    assert "TEMP-01" in strategy.alerts[0]
    assert "TEMP-02" in strategy.alerts[1]


def test_console_alert_strategy_execution(capsys):
    """La estrategia de consola debe imprimir la alerta formateada."""
    strategy = ConsoleAlertStrategy()
    detector = AnomalyDetector(strategy=strategy)

    detector.evaluate(sensor_id="PRES-01", value=110.0, threshold=100.0)

    captured = capsys.readouterr()
    assert "[ALERTA]" in captured.out
    assert "PRES-01" in captured.out