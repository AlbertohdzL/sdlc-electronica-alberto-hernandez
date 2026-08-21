# sdlc-electronica-alberto-hernandez
##  Despliegue y Producción

* **API en Producción:** [https://sensorhub-api-mqul.onrender.com](https://sensorhub-api-mqul.onrender.com)
* **Documentación Interactiva (Swagger):** [https://sensorhub-api-mqul.onrender.com/docs](https://sensorhub-api-mqul.onrender.com/docs)
* **Estado de Integración Continua (CI):** [![CI Pipeline](https://github.com/AlbertohdzL/sdlc-electronica-alberto-hernandez/actions/workflows/ci.yml/badge.svg)](https://github.com/AlbertohdzL/sdlc-electronica-alberto-hernandez/actions)

# 🛰️ SensorHub — Telemetry & IoT Anomaly Engine

Sistema de ingesta y monitoreo de telemetría IoT desarrollado con **FastAPI**, **SQLAlchemy 2.0** y **Pydantic v2**, estructurado bajo una **Arquitectura en 4 Capas** con Inversión de Dependencias (DIP) y cobertura de pruebas $\ge 90\%$.

---

## 🏛️ Arquitectura del Sistema

```mermaid
flowchart TD
    subgraph ClientLayer [Clientes IoT / Dashboard]
        HTTP[Petición HTTP / JSON]
    end

    subgraph Presentation [Capa de Presentación: Routers]
        R_Sensors[sensors.py]
        R_Readings[readings.py]
        R_Alerts[alerts.py]
    end

    subgraph Domain [Capa de Dominio: Servicios]
        S_Sensor[SensorService]
        S_Reading[ReadingService]
        S_Anomaly[AnomalyDetector]
        S_Alert[AlertService]
    end

    subgraph DataAccess [Capa de Persistencia: Repositorios]
        Repo_Sensor[(SensorRepository)]
        Repo_Reading[(ReadingRepository)]
        Repo_Alert[(AlertRepository)]
    end

    subgraph Database [Motor de Base de Datos]
        DB[(PostgreSQL / SQLite)]
    end

    HTTP --> R_Sensors & R_Readings & R_Alerts
    R_Sensors --> S_Sensor
    R_Readings --> S_Reading
    R_Alerts --> S_Alert
    S_Reading --> S_Anomaly
    S_Anomaly --> S_Alert
    S_Sensor --> Repo_Sensor
    S_Reading --> Repo_Reading
    S_Alert --> Repo_Alert
    Repo_Sensor & Repo_Reading & Repo_Alert --> DB