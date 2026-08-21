# 🤖 Bitácora de Ingeniería Asistida por IA (AI Log)

* **Proyecto:** SensorHub Telemetry API
* **Herramientas utilizadas:** Modelos LLM de asistencia en código y validación cruzada.
* **Periodo de desarrollo:** Semanas 1 a Final.

---

## 📌 Registro de Interacciones y Decisiones Clave

### 1. Refactorización a 4 Capas y DIP (Semana 3)
* **Objetivo:** Separar las dependencias de FastAPI y bases de datos relacionales de la lógica de dominio.
* **Intervención:** La IA propuso la estructura de repositorios bajo contratos `typing.Protocol` y servicios puros. Se revisaron y corrigieron rutas de importación circulares.

### 2. Detección de Anomalías y Estrategias OCP (Semana 4)
* **Objetivo:** Implementar la evaluación de umbrales en tiempo de ingesta sin acoplar la notificación.
* **Intervención:** Se aplicó el patrón Strategy (`AlertNotifier`, `FakeAlertNotifier`) para permitir verificar emisiones de alertas en memoria durante los tests unitarios sin emitir prints sucios en consola.

### 3. Soft Delete, Ciclo de Vida de Alertas y Estadísticas (Proyecto Final)
* **Objetivo:** Cumplir con la desactivación lógica (`is_active`), transiciones de alerta (`open` -> `acknowledged` -> `resolved`) y agregaciones numéricas SQL.
* **Intervención:** La IA detectó discrepancias en el serializador de Pydantic (`name` opcional) que bloqueaban 9 tests, ajustó el cálculo de agregaciones vía `func.avg`/`func.min`/`func.max` en SQLAlchemy y consolidó la suite a 27 pruebas con 90.15% de cobertura.
