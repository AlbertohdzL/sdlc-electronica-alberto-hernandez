# Bitácora de Uso de IA - Semana 1

## Entrada 1: 2026-07-13
* **Prompt enviado a la IA:** "Ayúdame a modelar una estructura para lecturas de sensores usando buenas prácticas de Python idiomático. Necesito representar tipos de sensores, estados de alerta, asegurar inmutabilidad y definir 5 funciones puras de procesamiento, además de un Protocol."
* **Código generado por la IA:** Propuso el uso de `Enum` para los tipos y estados, una `@dataclass(frozen=True)` para la lectura, y funciones que utilizan `dataclasses.replace` para mantener la pureza, junto con `typing.Protocol`.
* **Decisión de diseño y justificación:** Acepté el diseño completo porque soluciona de forma elegante el problema de la mutabilidad que sufríamos en sistemas embebidos convencionales. Mantener la lectura `frozen` previene efectos secundarios indeseados en canalizaciones de datos. El uso de `Protocol` permite la inyección de dependencias modular que se requerirá más adelante en la semana para SOLID sin la rigidez de la herencia múltiple de C++.
* **Detalle personal:** Aunque se que comento que esto solo es para practicar lo guardo aqui para tener a la mano lo que estudie y si lee esto y le es posible, le agredeceria que tambien me pudiera dar una retroalimentacion de este ejercicio de practica.

## Entrada 2: 2026-07-14
* **Prompt enviado a la IA:** "Con las ideas que te adjunte genera el código para fsm_demo.py y test_fsm.py basandote en ellas. La máquina debe ser orientada a objetos, usar un método explícito llamado transition(), ciclar entre RED, GREEN y YELLOW, y contar las vueltas completas. Además, incluye los 4 tests requeridos."
* **Código generado por la IA:** Diseñó la FSM usando una clase con propiedades de solo lectura para encapsular el estado y el contador, protegiendo las variables internas, junto con funciones de test independientes basadas en aserciones de pytest.
* **Decisión de diseño y justificación:** Se eliminó la idea de abstracción de las propiedades protegidas para evitar sobrecomplicar el diseño de software en esta etapa. En Python, el uso de atributos públicos es idiomático si no se requiere validación extra en la lectura. Esto mantiene el código limpio, plano y 100% defendible ante el coordinador, conservando la eficiencia de la tabla de búsqueda (diccionario) para las transiciones.

## Entrada 3: 2026-07-15
* **Prompt enviado a la IA:** "Ayúdame a optimizar el archivo solid_srp_ocp_lsp.py y su test correspondiente. Necesito que revises los ejemplos claros de 'Mal' y 'Bien' para los principios SRP, OCP y LSP aplicados al dominio de sensores, con 2 tests unitarios por principio."
* **Código generado por la IA:** Diseñó estructuras que separan el almacenamiento de la analítica (SRP), clases abstractas extendidas por polimorfismo para las alertas (OCP) y subclases que respetan los tipos de retorno numéricos sin romper el contrato del padre (LSP).
* **Decisión de diseño y justificación:** Se optó por el polimorfismo clásico de Python para OCP y LSP. Esto elimina la necesidad de modificar lógica existente cuando ingresa nuevo hardware al sistema, mitigando los riesgos de regresión comunes en el firmware tradicional.

## Entrada 4 : 2026-07-16
* **Prompt enviado a la IA:** "Revisa y optimisa el archivo solid_isp_dip.py y test_solid_isp_dip.py enfocado en los principios ISP y DIP usando typing.Protocol para inyección de dependencias en instrumentación."
* **Código generado por la IA:** Creó interfaces segregadas (ReaderProtocol y WriterProtocol) para cumplir con ISP, y un DataProcessor de alto nivel que recibe la interfaz por el constructor para cumplir con DIP.
* **Decisión de diseño y justificación:** El uso de `typing.Protocol` permite implementar desacoplamiento por Duck Typing estático. Al inyectar el protocolo en el constructor de la clase de alto nivel, el código queda 100% aislado del driver físico subyacente, facilitando el intercambio de hardware o la creación de Mocks en las pruebas sin alterar la lógica de negocio.