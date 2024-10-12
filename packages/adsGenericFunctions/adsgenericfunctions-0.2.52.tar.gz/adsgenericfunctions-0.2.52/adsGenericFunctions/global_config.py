_timer_enabled = False  # Initialisé à False


def set_timer(state: bool):
    global _timer_enabled
    _timer_enabled = state


def get_timer() -> bool:
    return _timer_enabled
