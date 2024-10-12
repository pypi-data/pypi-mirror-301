import timeit
from .global_config import get_timer

def timer(func):
    def wrapper(*args, **kwargs):
        if get_timer():
            logger = kwargs.get('logger')
            start_time = timeit.default_timer()
            result = func(*args, **kwargs)
            elapsed_time = timeit.default_timer() - start_time
            if logger is not None:
                logger.info(f"Temps d'exécution de {func.__name__}: {elapsed_time:.4f} secondes.")
            return result
        else:
            return func(*args, **kwargs)
    return wrapper