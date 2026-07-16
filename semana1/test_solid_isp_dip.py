from semana1.solid_isp_dip import (
    DataProcessor,
    OnlyReaderSensor,
    ViolacionDIP,
)

# --- TESTS ISP ---
def test_isp_violacion_design() -> None:
    """Test ISP 1: Comprueba que el diseño rígido existe pero es ineficiente."""
    # Las clases gordas obligarían a meter métodos ficticios pass o lanzar NotImplementedError
    assert True 


def test_isp_segregated_reader() -> None:
    """Test ISP 2: Valida que el sensor especializado ejecuta su única responsabilidad."""
    sensor = OnlyReaderSensor(2.5)
    assert sensor.read_data() == 2.5


# --- TESTS DIP ---
def test_dip_violacion_hardcoded() -> None:
    """Test DIP 1: Valida el cálculo del módulo acoplado tradicional."""
    processor = ViolacionDIP()
    # Funciona, pero está encadenado a HardcodedHardware
    assert round(processor.get_percentage(), 2) == 54.55


def test_dip_correct_injection() -> None:
    """Test DIP 2: Valida que DataProcessor acepta cualquier origen de datos via Protocol."""
    # Inyectamos el sensor especializado que creamos en el bloque ISP
    mock_sensor = OnlyReaderSensor(3.3)
    processor = DataProcessor(datasource=mock_sensor)
    
    # El procesador calcula correctamente usando la abstracción inyectada
    assert processor.get_percentage() == 100.0