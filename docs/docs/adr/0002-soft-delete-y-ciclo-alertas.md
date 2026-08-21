# ADR 0002: Desactivación Lógica (Soft Delete) y Ciclo de Vida de Alertas

## Estado
Aceptado

## Contexto
En sistemas de telemetría industrial, la eliminación física de un sensor destruye la integridad referencial de series temporales y auditorías. Asimismo, las anomalías detectadas requieren trazabilidad operativa por parte del equipo de monitoreo.

## Decisión
1. **Soft Delete (`is_active`):** El endpoint `DELETE /sensors/{sensor_id}` marca `is_active = False`. Las lecturas entrantes para sensores inactivos son rechazadas con error HTTP 400, preservando el histórico.
2. **Ciclo de Estados en Alertas:** Implementación de una máquina de estados finitos (`open` -> `acknowledged` -> `resolved`) gestionada mediante `PATCH /alerts/{id}`.

## Consecuencias
* **Positivas:** Cumplimiento de normativas de auditoría industrial, preservación íntegra de históricos y seguimiento de incidentes en tiempo real.
* **Negativas:** Consultas de sensores activos requieren filtrado explícito en la capa de persistencia.