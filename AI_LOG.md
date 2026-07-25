
## Semana 2 · Entrada 1: 2026-07-25 (Backlog y Criterios Gherkin)
* **Prompt enviado a la IA:** "Ayudame a terminar de estructura este Product Backlog con 10 User Stories para un sistema de monitoreo IoT de bodega industrial en formato Gherkin (Given/When/Then), estimación en Story Points y priorización MoSCoW."
* **Código generado por la IA:** Propuso 10 historias de usuario genéricas con escenarios Gherkin preliminares y estimaciones aleatorias.
* **Decisión de diseño y justificación:** Acepté la estructura de la plantilla y la sintaxis Gherkin. Ajusté los escenarios para el dominio real de la bodega industrial (rangos de temperatura de -50 °C a 100 °C, humedad de 0 % a 100 %, umbrales T > 35 °C y H > 80 %). Rechacé 2 escenarios por ser genéricos y no contener criterios de aceptación cuantitativos y verificables.

## Semana 2 · Entrada 2: 2026-07-25 (TDD en SensorReading y AnomalyDetector)
* **Prompt enviado a la IA:** "Genera pruebas unitarias en pytest para SensorReading y AnomalyDetector bajo TDD estricto con inyección de dependencias para los umbrales."
* **Código generado por la IA:** Sugirió clases con métodos de validación en Python y un archivo de pruebas unitarias.
* **Decisión de diseño y justificación:** Acepté el flujo Red-Green-Refactor. Modifiqué la sugerencia de la IA para implementar `SensorReading` como una dataclass inmutable (`frozen=True`) con validación en `__post_init__`. Aseguré que `AnomalyDetector` recibiera el umbral `max_threshold` en su constructor (DIP), evitando hardcodear valores en el código de producción.

## Semana 2 · Entrada 3: 2026-07-25 (Patrón Estrategia para Alertas)
* **Prompt enviado a la IA:** "Genera la implementación de AlertManager con el patrón Estrategia (ConsoleAlertStrategy y FileAlertStrategy) aplicando OCP y DIP, junto con sus pruebas unitarias en pytest."
* **Código generado por la IA:** Creó la clase abstracta `AlertStrategy` usando el módulo `abc`, sus dos subclases concretas y el orquestador `AlertManager`, además de pruebas unitarias asociadas.
* **Decisión de diseño y justificación:** Acepté el patrón Estrategia por cumplir con los principios OCP y DIP. En las pruebas de `FileAlertStrategy`, rechacé la ruta de archivo estática sugerida por la IA y la reemplacé por el fixture `tmp_path` de `pytest` para aislar las pruebas de E/S y evitar la contaminación del directorio de trabajo.
