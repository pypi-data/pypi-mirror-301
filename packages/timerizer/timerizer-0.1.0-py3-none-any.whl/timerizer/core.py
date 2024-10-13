import time
import functools

def timer(func):
    """
    Decorator that prints the runtime of the decorated function.
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {run_time:.4f} seconds")
        return value
    return wrapper_timer
