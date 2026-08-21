# ADR 0001: Arquitectura en capas para SensorHub

## Estado
**Aceptado**

## Contexto
El sistema SensorHub requiere gestionar la telemetría de dispositivos IoT, procesar reglas de validación de física real y persistir datos. En fases tempranas, acoplar las rutas HTTP directamente a consultas SQL o modelos de base de datos impedía probar la lógica de negocio de forma aislada y ataba el proyecto a un motor de base de datos específico (como SQLite en pruebas locales vs. PostgreSQL en producción).

Necesitábamos una estructura desacoplada que permitiera:
1. Probar la lógica de validación e ingesta sin levantar una base de datos real ni el servidor HTTP.
2. Cambiar de proveedor de base de datos (o usar PostgreSQL en CI/producción y fakes en testing) sin modificar los endpoints ni las reglas del negocio.
3. Mantener responsabilidades claras para facilitar el mantenimiento y la colaboración bajo metodología ágil.

## Decisión
Implementamos una **Arquitectura en 4 Capas** aplicando el **Principio de Inversión de Dependencias (DIP)**[cite: 1]:

[ Routers / Presentación ] (FastAPI HTTP, validación Pydantic In/Out)
│
▼
[ Services / Negocio ] (Reglas físicas, orquestación, excepciones de dominio)
│
▼
[ Repositories / Acceso a Datos ] (Protocol/Abstracción -> SQLAlchemy Queries)
│
▼
[ Models / Persistencia ] (Tablas y esquemas ORM de base de datos)

- **Routers (`app/routers/`):** Gestionan el transporte HTTP, serialización y códigos de estado[cite: 1].
- **Services (`app/services/`):** Contienen exclusivamente la lógica de negocio y validación física[cite: 1].
- **Repositories (`app/repositories/`):** Encapsulan el acceso a la base de datos detrás de una abstracción[cite: 1].
- **Models (`app/models/`):** Definición de esquemas de tablas relacionales[cite: 1].

## Consecuencias

### Positivas (+)
* **Alta Testabilidad:** Permite probar el 100% de la lógica de servicios inyectando repositorios simulados (*mocks* o *in-memory fakes*) sin tocar la base de datos real ni requerir transacciones lentas[cite: 1].
* **Desacoplamiento de Infraestructura:** La transición de SQLite a PostgreSQL en Docker/Render se realiza únicamente configurando la URL de conexión en la capa de datos, sin alterar los routers ni los servicios[cite: 1].
* **Mantenibilidad:** Cada archivo tiene una única responsabilidad clara (SRP)[cite: 1].

### Negativas / Costos (-)
* **Mayor Ceremonia de Archivos:** Agregar una nueva funcionalidad requiere tocar 4 capas distintas (Router, Service, Repository, Model/Schema) en lugar de un script único[cite: 1].
* **Sobrecarga Inicial de Abstracción:** Para operaciones CRUD elementales, el código puede parecer redundante, pero el beneficio se paga en escalabilidad y robustez de pruebas[cite: 1].

## Alternativas Descartadas
1. **Script Monolítico / Arquitectura en 1 Capa (FastAPI directo a SQL):** Se descartó porque acopla la lógica de negocio al framework web y hace inviable alcanzar una cobertura de tests sólida sin levantar bases de datos temporales en cada ejecución[cite: 1].
2. **Microservicios Prematuros:** Se descartó porque introduce complejidad de red, latencia y sobrecarga operacional innecesaria para la etapa actual del producto[cite: 1].