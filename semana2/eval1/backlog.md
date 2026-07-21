# Product Backlog — Sistema de Monitoreo IoT para Bodega Industrial

## Contexto del Proyecto
Este Product Backlog pertenece al sistema de monitoreo IoT para una bodega industrial. El sistema gestiona la telemetría de 10 sensores de temperatura y humedad que transmiten lecturas cada 30 segundos, realizando detección automática de anomalías (Temperatura > 35 °C o Humedad > 80 %) y despachando alertas[cite: 1].

---

## Criterios de Estimación y Priorización

### Criterios de Priorización (MoSCoW)
* **Must Have (M):** Requisitos imprescindibles para la operación básica e inmediata del Sprint 1.
* **Should Have (S):** Funcionalidades importantes que aportan valor pero no bloquean la salida a producción.
* **Could Have (C):** Funcionalidades deseables o de extensión que se implementan si hay capacidad restante.
* **Won't Have (W):** Requisitos fuera del alcance para este primer ciclo.

### Escala de Estimación (Story Points)
Se utiliza la secuencia de Fibonacci (**1, 2, 3, 5, 8**) para evaluar la complejidad relativa, riesgo e incertidumbre técnica de cada historia, no las horas hombre.

---

# User Stories

## US-01: Ingesta y validación de lecturas de sensores
* **Prioridad:** Must Have
* **Estimación:** 3 Story Points
* **Rol:** Operador de planta

**Descripción:**
Como operador de planta,
quiero que el sistema valide los datos de temperatura y humedad entrantes,
para descartar lecturas corruptas o fuera de rango físico.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Recepción de una lectura válida de temperatura
  Given un sensor activo con ID "TEMP-01" en la bodega
  When se envía una lectura de temperatura con valor 24.5 °C y timestamp actual
  Then el sistema acepta la lectura y la marca con estado "OK"

Scenario: Rechazo de lectura fuera de rango físico extremo
  Given un sensor activo con ID "TEMP-01" en la bodega
  When se envía una lectura de temperatura con valor -300.0 °C
  Then el sistema rechaza la lectura lanzando un error de validación física
```

## US-02: Detección automática de anomalías
* **Prioridad:** Must Have
* **Estimación:** 3 Story Points
* **Rol:** Sistema de monitoreo

**Descripcion**
Como sistema de monitoreo,
quiero evaluar cada lectura recibida contra los umbrales del sensor,
para identificar inmediatamente si la bodega supera los límites seguros.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Detección de anomalía por alta temperatura
  Given un sensor de temperatura "TEMP-02" con umbral inyectado de 35.0 °C
  When se procesa una lectura de 36.5 °C
  Then el sistema clasifica la lectura como una anomalía
  And genera un evento de alerta crítica

Scenario: Lectura dentro del rango normal de operación
  Given un sensor de humedad "HUM-01" con umbral inyectado de 80.0 %
  When se procesa una lectura de 65.0 %
  Then el sistema determina que el estado es normal
  And no genera ningún evento de alerta
```

## US-03: Detección automática de anomalías
* **Prioridad:** Must Have
* **Estimación:** 5 Story Points
* **Rol:** Administrador de seguridad industrial

**Descripcion**
Como administrador de seguridad industrial,
quiero que las alertas generadas por anomalías se envíen mediante estrategias configurables,
para registrar los eventos tanto en consola como en archivo local sin acoplar la lógica.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Emisión de alerta por consola y archivo
  Given un detector de anomalías configurado con FileAlertStrategy y ConsoleAlertStrategy
  When el detector procesa una anomalía en el sensor "HUM-03" (85.0 %)
  Then la estrategia escribe el mensaje de alerta en el log de consola
  And la estrategia escribe la alerta formateada en el archivo "alerts.log"
```

## US-04: Registro centralizado de sensores
* **Prioridad:** Must Have
* **Estimación:** 2 Story Points
* **Rol:** Técnico de mantenimiento

**Descripcion**
Como técnico de mantenimiento,
quiero registrar y consultar los metadatos de los 10 sensores de la bodega,
para tener trazabilidad del tipo de variable y ubicación física de cada dispositivo.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Consulta de un sensor registrado existente
  Given que el sensor "TEMP-05" está registrado en la ubicación "Pasillo A"
  When solicito la información del sensor "TEMP-05"
  Then el sistema retorna la ubicación "Pasillo A" y el tipo "Temperatura"

Scenario: Intento de consulta de un sensor no registrado
  Given que no existe ningún sensor registrado con ID "GHOST-99"
  When solicito la información del sensor "GHOST-99"
  Then el sistema lanza una excepción "SensorNotFoundError"
```

## US-05: Modificación dinámica de umbrales
* **Prioridad:** Should Have
* **Estimación:** 2 Story Points
* **Rol:** Jefe de calidad de insumos

**Descripcion**
Como jefe de calidad de insumos,
quiero actualizar el umbral máximo tolerado de un sensor específico,
para ajustar los criterios de anomalía según la temporada o tipo de producto almacenado.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Actualización exitosa del umbral de alerta
  Given el sensor "TEMP-01" con un umbral inicial de 35.0 °C
  When actualizo el umbral del sensor "TEMP-01" a 30.0 °C
  And se procesa una lectura de 32.0 °C
  Then el sistema detecta la anomalía usando el nuevo umbral de 30.0 °C
```

## US-06: Historial de lecturas por sensor
* **Prioridad:** Should Have
* **Estimación:** 3 Story Points
* **Rol:** Auditor de seguridad

**Descripcion**
Como auditor de seguridad,
quiero consultar el historial de mediciones de un sensor específico,
para analizar la tendencia térmica o de humedad durante un turno de trabajo.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Obtención del historial de mediciones registradas
  Given que el sensor "HUM-02" ha registrado 5 lecturas válidas
  When solicito el historial del sensor "HUM-02"
  Then el sistema retorna una lista con las 5 lecturas ordenadas cronológicamente
```

## US-07: Reconocimiento y cierre de alertas
* **Prioridad:** Should Have
* **Estimación:** 2 Story Points
* **Rol:** Operador de planta

**Descripcion**
Como operador de planta,
quiero cambiar el estado de una alerta activa a "Reconocida",
para indicar al equipo que la anomalía en la bodega ya está siendo atendida.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Cambio de estado de una alerta abierta a reconocida
  Given una alerta activa en estado "OPEN" para el sensor "TEMP-04"
  When el operador marca la alerta como "ACKNOWLEDGED"
  Then el estado de la alerta se actualiza a "ACKNOWLEDGED"
```

## US-08: Persistencia de respaldo ante fallos de alerta
* **Prioridad:** Could Have
* **Estimación:** 3 Story Points
* **Rol:** Sistema de monitoreo

**Descripcion**
Como sistema de monitoreo,
quiero escribir las alertas no entregadas en un buffer de respaldo en disco,
para garantizar la cero pérdida de eventos críticos si falla el canal primario.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Fallo de alerta primaria redirigido a respaldo
  Given que la alerta por correo electrónico falla por desconexión
  When se intenta despachar una alerta crítica del sensor "TEMP-02"
  Then el sistema guarda el evento en el archivo de respaldo "fallback_alerts.jsonl"
```

## US-09: Simulación de sensores con distribución Gaussiana
* **Prioridad:** Could Have (Extensión)
* **Estimación:** 5 Story Points
* **Rol:** Desarrollador de pruebas

**Descripcion**
Como desarrollador de pruebas,
quiero simular el comportamiento de 10 sensores generando ruido gaussiano realista,
para verificar la carga y resiliencia del sistema durante 60 ciclos de monitoreo.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Generación de mediciones simuladas con distribución normal
  Given un simulador de sensores configurado con media de 25.0 °C y desviación de 2.0 °C
  When ejecuto la simulación por 60 ciclos para 10 sensores
  Then el sistema genera 600 lecturas dentro de los intervalos estadísticos esperados
```

## US-10: Vista consolidada de métricas de bodega
* **Prioridad:** Won't Have (Fuera de alcance del Sprint 1)
* **Estimación:** 8 Story Points
* **Rol:** Gerente de operaciones

**Descripcion**
Como gerente de operaciones,
quiero ver un tablero gráfico web en tiempo real con el estado de todos los sensores,
para tomar decisiones estratégicas sobre el consumo energético de la bodega.

**Criterios de Aceptación (Gherkin):**
```gherkin
Scenario: Renderizado de dashboard web
  Given una sesión iniciada como gerente de operaciones
  When navego a la ruta "/dashboard"
  Then el sistema muestra los gráficos de temperatura y humedad de la bodega
```