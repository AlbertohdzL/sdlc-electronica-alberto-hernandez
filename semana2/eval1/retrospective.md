# Sprint 1 Retrospective — Sistema de Monitoreo IoT

## 🌟 1. ¿Qué salió bien? (What went well)
* **Disciplina TDD Estricta:** Se mantuvo de forma impecable el ciclo **Red → Green → Refactor** en el historial de Git para cada una de las 3 historias del núcleo (`US-01`, `US-02` y `US-03`)[cite: 1].
* **Diseño Orientado a Objetos y SOLID:** La aplicación de Inversión de Dependencias (DIP) y Abierto/Cerrado (OCP) mediante el patrón Estrategia en `AlertManager` y la inyección de umbrales en `AnomalyDetector` permitió crear un código altamente flexible y fácilmente testeable[cite: 1].
* **Calidad de Código Sobresaliente:** Se logró una cobertura de pruebas del 100% en los módulos del núcleo, manteniendo `ruff` y `mypy` totalmente limpios[cite: 1].

---

## 🔻 2. ¿Qué se puede mejorar? (What could be improved)
* **Resolución de Módulos en Python/Pytest:** Al inicio surgieron pequeñas confusiones con la importación de submódulos en pruebas unitarias debido al manejo de rutas de paquetes.
* **Granularidad de Commits:** En ocasiones es tentador escribir la solución completa antes de guardar el commit de la fase RED. Se debe reforzar el hábito de pausar e independizar cada commit.

---

## 🎯 3. Acción Concreta de Mejora (Action Item)
* **Acción:** Crear un script de automatización local o pre-commit hook que ejecute en secuencia `ruff check`, `mypy` y `pytest --cov` antes de realizar un `git push`, garantizando que ningún commit invalide la *Definition of Done*[cite: 1].