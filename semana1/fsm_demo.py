from enum import Enum, auto


class TrafficLightState(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()


class TrafficLightFSM:

    def __init__(self) -> None:
        # Estado actual del semáforo; comienza en ROJO.
        self.state: TrafficLightState = TrafficLightState.RED
        # Contador de ciclos completos que pasan por ROJO nuevamente.
        self.cycle_count: int = 0

    def transition(self) -> TrafficLightState:
        """Cambia al siguiente estado del semáforo y actualiza el contador de los ciclos."""
        transitions = {
            TrafficLightState.RED: TrafficLightState.GREEN,
            TrafficLightState.GREEN: TrafficLightState.YELLOW,
            TrafficLightState.YELLOW: TrafficLightState.RED,
        }

        # Obtenemos el siguiente estado a partir del estado actual.
        self.state = transitions[self.state]

        # Cada vez que regresamos a ROJO, contamos un ciclo completo en el contador.
        if self.state == TrafficLightState.RED:
            self.cycle_count += 1

        return self.state


if __name__ == "__main__":
    import time

    # Creamos una instancia de la máquina de estados del semáforo.
    semaforo = TrafficLightFSM()
    print(f"Estado inicial: {semaforo.state}")

    try:
        while True:
            # Espera 1 segundo entre cada cambio de estado.
            time.sleep(1)
            nuevo_estado = semaforo.transition()
            # Imprime el nombre del estado y el número de ciclos completos.
            print(
                f"Estado: {nuevo_estado.name} | Ciclos: {semaforo.cycle_count}"
            )
    except KeyboardInterrupt:
        print("\nSimulación detenida.")