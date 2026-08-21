# ADR 0001: Adopción de Arquitectura en 4 Capas con Inversión de Dependencias (DIP)

## Estado
Aceptado

## Contexto
SensorHub requiere procesar flujos de telemetría IoT garantizando alta mantenibilidad, testabilidad unitaria aislada y desacoplamiento estricto del framework web (FastAPI) y la capa de persistencia (SQLAlchemy / PostgreSQL).

## Decisión
Dividir el sistema en 4 capas desacopladas siguiendo el principio de inversión de dependencias (DIP):
1. **Modelos / Schemas:** Definición de entidades ORM y validación de esquemas con Pydantic v2.
2. **Repositorios:** Encapsulamiento del acceso a datos con métodos específicos (`SensorRepository`, `AlertRepository`, `ReadingRepository`).
3. **Servicios:** Centralización de las reglas de dominio, validaciones físicas y detección de anomalías sin dependencias HTTP.
4. **Routers:** Adaptadores de transporte HTTP encargados de códigos de estado, inyección de dependencias y serialización.

## Consecuencias
* **Positivas:** Cobertura de pruebas superior al 90% mediante dobles de prueba sin levantar base de datos real en pruebas unitarias; fácil sustitución de motores SQL.
* **Negativas:** Mayor número de archivos y clases intermedias.