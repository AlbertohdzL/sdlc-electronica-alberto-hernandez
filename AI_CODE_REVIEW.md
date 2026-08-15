# AI Code Review · Semana 5

**Clase Auditada:** `app/services/sensor_service.py`  
**Herramienta de IA:** Copilot Chat / Gemini  

## Prompt Utilizado
> "Revisa esta clase como un ingeniero senior en un code review. Busca: violaciones de SOLID, casos borde sin manejar, riesgos de seguridad y problemas de rendimiento. Para cada hallazgo indica la línea y propone una corrección. No reescribas todo; solo señala."

## Hallazgos Detectados
---

### 1. [SOLID - SRP / DIP] Acoplamiento con el Framework Web (`HTTPException`)

* **Líneas:** 3, 19–22, 28–31, 45–48, 56–59


* **Tipo:** Violación de Arquitectura y Principio de Responsabilidad Única (SRP).
* **Descripción:** La capa de servicio (`services/`) importa y lanza excepciones directas de FastAPI (`HTTPException`). La lógica de negocio debe permanecer agnóstica al transporte (HTTP, CLI, gRPC, etc.). Si el día de mañana usas esta clase en una tarea en segundo plano (Celery) o un cliente MQTT, fallará con excepciones web fuera de contexto.


* **Propuesta de corrección:**
Crea excepciones de dominio puras (ej. `SensorNotFoundError`, `SensorAlreadyExistsError`). Haz que el servicio las lance y que sea la capa de presentación (`routers/`) o un middleware global de FastAPI quien las capture y traduzca a respuestas `HTTPException` con sus códigos correspondientes (404, 409).



---

### 2. [Riesgo de Seguridad / Rendimiento] Paginación Sin Límites Supriores (Vulnerabilidad DoS)

* **Línea:** 36


* **Tipo:** Problema de Rendimiento y Seguridad (Exhaustión de Memoria).
* **Descripción:** El método `list_sensors` recibe `limit` y `offset` sin acotación previa. Un atacante podría enviar `limit=1000000`, obligando a la base de datos a cargar miles de registros a la memoria en una sola petición, colapsando el contenedor.


* **Propuesta de corrección:**
Sanitiza y limita los parámetros al inicio del método:
```python
limit = max(1, min(limit, 100))  # Limita entre 1 y 100 registros como máximo
offset = max(0, offset)

```



---

### 3. [Riesgo de Seguridad / Concurrencia] Condición de Carrera en Creación (*TOCTOU*)

* **Líneas:** 17–23


* **Tipo:** Condición de carrera (Time-of-Check to Time-of-Use).
* **Descripción:** La secuencia `get_by_sensor_id` seguida de `create` no es atómica. En entornos de alta concurrencia, si dos peticiones crean el mismo `sensor_id` exactamente al mismo tiempo, ambas verificarán que "no existe" y ambas intentarán insertar, lanzando un error no controlado de base de datos (`IntegrityError` / 500 Internal Server Error) en la segunda inserción.


* **Propuesta de corrección:**
Confía en el índice de unicidad (`UNIQUE`) de la base de datos. Intenta crear directamente y captura la excepción de integridad en el repositorio o servicio para convertirla en un error de conflicto.

---

### 4. [SOLID - DIP] Dependencia de una Clase Concreta

* **Líneas:** 4, 12


* **Tipo:** Violación del Principio de Inversión de Dependencias (DIP).
* **Descripción:** `__init__` anota el parámetro `repository` directamente con la clase concreta `SensorRepository`.


* **Propuesta de corrección:**
Define un protocolo/interfaz (`SensorRepositoryProtocol`) usando `typing.Protocol`. De este modo, la clase dependerá de una abstracción y facilitará la inyección de repositorios simulados (*fakes/mocks*) en las pruebas unitarias sin tocar la base de datos real.



---

### 5. [Caso Borde / Sanitización] Limpieza de Identificadores (`sensor_id`)

* **Líneas:** 15, 26, 41, 52


* **Tipo:** Caso borde sin manejar.
* **Descripción:** Los identificadores se reciben sin sanitizar. Un `sensor_id` enviado con espacios al inicio o final (ej. `" TEMP-01 "`) o compuesto solo por espacios vacíos generará inconsistencias en la base de datos.
* **Propuesta de corrección:**
Asegura la sanitización al inicio de los métodos o fuerza que el esquema Pydantic (`SensorCreate`) aplique `.strip()` y valide el formato con una expresión regular antes de llegar al servicio.