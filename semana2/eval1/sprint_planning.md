# Sprint 1 Planning — Sistema de Monitoreo IoT para Bodega Industrial

## 🎯 Sprint Goal
Construir y validar el núcleo del sistema de monitoreo IoT capaz de validar lecturas de temperatura y humedad, evaluar anomalías mediante umbrales inyectados y despachar alertas a consola y archivo con una cobertura de pruebas ≥ 80% y TDD estricto.

---

## 📊 Historias de Usuario Seleccionadas (Sprint Backlog)

| ID | Título | Story Points | Prioridad MoSCoW | Justificación de Selección |
|---|---|---|---|---|
| **US-01** | Ingesta y validación de lecturas de sensores | 3 | Must Have | Fundamento del sistema: garantiza la integridad física de los datos de entrada. |
| **US-02** | Detección automática de anomalías | 3 | Must Have | Lógica central de negocio: evalúa las lecturas contra umbrales seguros. |
| **US-03** | Despacho y estrategia de alertas | 5 | Must Have | Salida de valor: notifica las anomalías detectadas sin acoplar los medios de transporte. |

**Capacidad Total del Sprint:** 11 Story Points (100% de la funcionalidad del núcleo requerida para la Evaluación 1).

---

## 🛠️ Desglose de Tareas Tecnológicas (Estimación ≤ 4 h por tarea)

### Para US-01: Ingesta y validación de lecturas (3 SP)
- [x] **TSK-1.1 (1.5 h):** Escribir pruebas unitarias iniciales en `test_sensor_reading.py` para rangos válidos e inválidos (Fase RED).
- [x] **TSK-1.2 (2.0 h):** Implementar la dataclass inmutable `SensorReading` con validaciones en `__post_init__` (Fase GREEN).
- [x] **TSK-1.3 (0.5 h):** Refactorizar y verificar cumplimiento de estilos con `ruff` y `mypy` (Fase REFACTOR).

### Para US-02: Detección de anomalías (3 SP)
- [x] **TSK-2.1 (1.0 h):** Escribir pruebas unitarias en `test_anomaly_detector.py` para evaluación de umbrales inyectados (Fase RED).
- [x] **TSK-2.2 (1.5 h):** Implementar la clase `AnomalyDetector` desacoplada con inyección de dependencias (Fase GREEN).
- [x] **TSK-2.3 (0.5 h):** Validar tipado y cobertura de pruebas.

### Para US-03: Despacho de alertas (5 SP)
- [x] **TSK-3.1 (2.0 h):** Escribir pruebas unitarias en `test_alert_manager.py` usando fixtures de captura de salida y archivos temporales (Fase RED)[cite: 1].
- [x] **TSK-3.2 (2.5 h):** Implementar la interfaz `AlertStrategy` y las clases concretas `ConsoleAlertStrategy`, `FileAlertStrategy` y `AlertManager` (Fase GREEN)[cite: 1].
- [x] **TSK-3.3 (0.5 h):** Ejecutar análisis estático y asegurar cobertura global ≥ 80%[cite: 1].

---

## ⚙️ Alineación con la Definition of Done (DoD)
El incremento resultante de este Sprint solo se considerará completado al cumplir la `DEFINITION_OF_DONE.md` del proyecto: pruebas en verde, linters `ruff` y `mypy` sin errores, commits atómicos en Git con secuencia TDD y bitácora de IA actualizada[cite: 1].