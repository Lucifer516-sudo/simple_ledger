from typing import Callable
from time import perf_counter, perf_counter_ns
from simple_ledger.utils.rich_printing._get_console import get_console
from functools import wraps

console = get_console()


def timer(func: Callable, console=console):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        _ = func(*args, **kwargs)
        stop = perf_counter()
        console.log(
            f"Time Taken to Execute the function `{func.__name__}` is: {round((stop-start)/60, 3)} min [or] {round((stop-start), 3)} sec"
        )
        return _

    return wrapper
