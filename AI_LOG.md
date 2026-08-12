
## Semana 2 · Entrada 1: 2026-07-25 (Backlog y Criterios Gherkin)
* **Prompt enviado a la IA:** "Ayudame a terminar de estructura este Product Backlog con 10 User Stories para un sistema de monitoreo IoT de bodega industrial en formato Gherkin (Given/When/Then), estimación en Story Points y priorización MoSCoW."
* **Código generado por la IA:** Propuso 10 historias de usuario genéricas con escenarios Gherkin preliminares y estimaciones aleatorias.
* **Decisión de diseño y justificación:** Acepté la estructura de la plantilla y la sintaxis Gherkin. Ajusté los escenarios para el dominio real de la bodega industrial (rangos de temperatura de -50 °C a 100 °C, humedad de 0 % a 100 %, umbrales T > 35 °C y H > 80 %). Rechacé 2 escenarios por ser genéricos y no contener criterios de aceptación cuantitativos y verificables.

## Semana 2 · Entrada 2: 2026-07-25 (TDD en SensorReading y AnomalyDetector)
* **Prompt enviado a la IA:** "Genera pruebas unitarias en pytest para SensorReading y AnomalyDetector bajo TDD estricto con inyección de dependencias para los umbrales."
* **Código generado por la IA:** Sugirió clases con métodos de validación en Python y un archivo de pruebas unitarias.
* **Decisión de diseño y justificación:** Acepté el flujo Red-Green-Refactor. Modifiqué la sugerencia de la IA para implementar `SensorReading` como una dataclass inmutable (`frozen=True`) con validación en `__post_init__`. Aseguré que `AnomalyDetector` recibiera el umbral `max_threshold` en su constructor (DIP), evitando hardcodear valores en el código de producción.

## Semana 2 · Entrada 3: 2026-07-25 (Patrón Estrategia para Alertas)
* **Prompt enviado a la IA:** "Dame ideas para mejorar la implementación de AlertManager con el patrón Estrategia (ConsoleAlertStrategy y FileAlertStrategy) aplicando OCP y DIP, junto con sus pruebas unitarias en pytest."
* **Código generado por la IA:** Creó la clase abstracta `AlertStrategy` usando el módulo `abc`, sus dos subclases concretas y el orquestador `AlertManager`, además de pruebas unitarias asociadas.
* **Decisión de diseño y justificación:** Acepté el patrón Estrategia por cumplir con los principios OCP y DIP. En las pruebas de `FileAlertStrategy`, rechacé la ruta de archivo estática sugerida por la IA y la reemplacé por el fixture `tmp_path` de `pytest` para aislar las pruebas de E/S y evitar la contaminación del directorio de trabajo.

## Semana 3 · Entrada 1: 2026-08-01 (Arquitectura en 4 Capas y Validación Pydantic)
* **Prompt enviado a la IA:** "Ayudame a terminar de diseñar los esquemas Pydantic para un recurso Reading que valide límites físicos reales de temperatura y humedad, y desacopla la aplicación en 4 capas (routers -> services -> repositories -> models)."
* **Código generado por la IA:** Propuso esquemas Pydantic con validadores genéricos y sugirió usar la API antigua de SQLAlchemy (Column).
* **Decisión de diseño y justificación:** Acepté la estructura en 4 capas para cumplir con DIP a escala de aplicación. Modifiqué los esquemas Pydantic implementando `@model_validator(mode="after")` para validar la coherencia física real (temperatura en °C entre -50 y 100, humedad en % entre 0 y 100). Rechacé el código de SQLAlchemy 1.x y lo actualicé a SQLAlchemy 2.0 tipado con `Mapped[...]` para garantizar la compatibilidad con mypy.

## Semana 3 · Entrada 2: 2026-08-01 (Manejo Exclusivo de Excepciones HTTP 4XX)
* **Prompt enviado a la IA:** "Asi deberia implementar la capa de servicios (SensorService y ReadingService)? para traducir fallos de reglas de negocio a excepciones HTTP 4XX precisas."
* **Código generado por la IA:** Generó capturas genéricas de excepciones `ValueError` y retornaba código 500 ante errores de negocio.
* **Decisión de diseño y justificación:** Rechacé el código 500 y refactoricé los servicios para mapear explícitamente cada fallo a la familia 4XX: `409 Conflict` cuando el `sensor_id` ya existe, `404 Not Found` cuando el recurso no se localiza, y `400 Bad Request` si se intenta registrar una lectura en un sensor deshabilitado. Esto cumple con las convenciones REST estándar.

## Semana 3 · Entrada 3: 2026-08-01 (Pruebas de Integración con TestClient e In-Memory DB)
* **Prompt enviado a la IA:** "Dame ideas para crear la suite de pruebas de integración con TestClient de FastAPI y un fixture de pytest para SQLite en memoria."
* **Código generado por la IA:** Sugirió pruebas reutilizando la base de datos `sensorhub.db` física en disco.
* **Decisión de diseño y justificación:** Rechacé el uso de la BD en disco en las pruebas para evitar la contaminación de datos entre ejecuciones. Implementé un fixture en `tests/conftest.py` con `sqlite:///:memory:` y `StaticPool`, anulando la dependencia `get_db` con `app.dependency_overrides`. Logramos una cobertura del 91% en la carpeta `app/`.


## Semana 5 
Dato importante: Para que funcione bien el pytest y se pueda apreciar de manera correcta el resultado utilice el siguiente comando:
python3 -m pytest semana5/ -o addopts="" --cov=semana5 --cov-fail-under=80
## Semana 5 · Entrada 1
**Herramienta usada:** Copilot Chat / Aider
**Prompt:** "Genera la función fahrenheit_to_celsius(f: float) -> float validando el cero absoluto físico (-459.67 °F) y redondeando a 2 decimales, junto con sus tests pytest."
**Resultado de la IA:** Propuso la implementación matemática y 4 escenarios de prueba.
**Decisión:** **Aceptado con modificaciones.**
- *Aceptado:* La lógica de conversión y la validación de la excepción `ValueError`.
- *Modificado:* Se ajustó la firma del test para coincidir con las convenciones de nombres del proyecto (`test_fahrenheit_to_celsius_valid`).