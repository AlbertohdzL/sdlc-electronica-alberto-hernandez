from semana1.fsm_demo import TrafficLightFSM, TrafficLightState


def test_initial_state() -> None:
    """Prueba 1: Valida que el estado de arranque sea estrictamente RED."""
    fsm = TrafficLightFSM()
    assert fsm.state == TrafficLightState.RED
    assert fsm.cycle_count == 0


def test_transition_red_to_green() -> None:
    """Prueba 2: Valida la transición directa del estado RED a GREEN."""
    fsm = TrafficLightFSM()
    fsm.transition()
    assert fsm.state == TrafficLightState.GREEN


def test_complete_cycle_returns_to_red() -> None:
    """Prueba 3: Valida que un ciclo completo regrese la máquina al estado RED."""
    fsm = TrafficLightFSM()
    fsm.transition()  # A GREEN
    fsm.transition()  # A YELLOW
    fsm.transition()  # A RED
    assert fsm.state == TrafficLightState.RED


def test_cycle_counter_increments() -> None:
    """Prueba 4: Valida el incremento preciso del contador de vueltas."""
    fsm = TrafficLightFSM()

    # Primera vuelta completa
    fsm.transition()
    fsm.transition()
    fsm.transition()
    assert fsm.cycle_count == 1

    # Segunda vuelta completa
    fsm.transition()
    fsm.transition()
    fsm.transition()
    assert fsm.cycle_count == 2