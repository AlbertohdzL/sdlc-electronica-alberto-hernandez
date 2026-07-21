# Definition of Done (DoD) — Sistema de Monitoreo IoT (Sprint 1)

Este documento establece los criterios explícitos e innegociables de calidad que debe cumplir cada User Story para pasar de la columna **In Progress** / **Review** a **Done** en el tablero de trabajo.

---

## 1. 🧪 Pruebas Automatizadas y TDD (Test-Driven Development)
- [ ] **Evidencia de TDD:** Existe al menos un ciclo de commits verificable en Git con la secuencia **Red** (test fallido) $\rightarrow$ **Green** (código mínimo que pasa) $\rightarrow$ **Refactor** (mejora limpia).
- [ ] **Traducción de Criterios:** Todos los escenarios Gherkin definidos en la User Story están traducidos a pruebas unitarias o de integración en `pytest`.
- [ ] **Cero Tests Triviales:** No se incluyen tests vacíos o redundantes únicamente para inflar métricas.
- [ ] **Cobertura de Código:** La suite de pruebas alcanza una cobertura de líneas $\ge 80\%$ comprobada con `pytest --cov`.

---

## 2. 🧹 Calidad Estática de Código y Estilo
- [ ] **Linter Limpio:** El comando `ruff check semana2/eval1/` se ejecuta sin errores ni advertencias de estilo o formato.
- [ ] **Tipado Estricto:** El comando `mypy semana2/eval1/` aprueba sin errores de tipado estático (todas las funciones y métodos cuentan con *type hints* completos en parámetros y retornos).
- [ ] **Principios SOLID:** La implementación aplica inyección de dependencias (DIP) y desacoplamiento de responsabilidades (SRP, OCP). No existen umbrales ni rutas *hardcodeadas*.

---

## 3. 🔍 Revisión y Control de Versiones
- [ ] **Commits Atómicos:** Los cambios se dividen en commits pequeños con mensajes descriptivos siguiendo convenciones semánticas (`feat`, `fix`, `test`, `refactor`, `docs`).
- [ ] **Auto-revisión de Diff:** Se inspeccionó el `git diff` completo antes de hacer *merge* para asegurar que no se filtren archivos temporales, comentarios obsoletos o código muerto.
- [ ] **Rama Limpia:** La rama principal (`main`) se mantiene funcional y sin pruebas rotas.

---

## 4. 📝 Documentación y Trazabilidad
- [ ] **Bitácora de IA:** Cualquier interacción con herramientas de IA (Copilot, ChatGPT, etc.) relacionada con la historia está registrada en `AI_LOG.md` detallando el prompt, el resultado y la justificación técnica de aceptación/rechazo.
- [ ] **Docstrings:** Las clases e interfaces principales cuentan con documentación de código clara que explica sus responsabilidades y contratos de excepción.