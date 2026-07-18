"""Módulo encargado de la persistencia de datos (Recorder) en formato JSON-lines."""

import json


class DataRecorder:
    """Clase especializada en el almacenamiento de datos en disco.

    Aplica el principio SRP al aislar las operaciones de Entrada/Salida (I/O)
    de la lógica de parsing o del estado del puerto UART.
    """

    def __init__(self, filepath: str) -> None:
        """Inicializa el recorder asignándole una ruta de archivo destino."""
        self.filepath = filepath

    def record(self, data: dict) -> None:
        """Escribe un diccionario de datos como una nueva línea en formato JSON-lines.

        Abre el archivo en modo append ('a') para asegurar un flujo eficiente
        y no destructivo de la telemetría.
        """
        # Convertimos el diccionario a un string JSON y le añadimos un salto de línea
        json_string = json.dumps(data) + "\n"
        
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json_string)