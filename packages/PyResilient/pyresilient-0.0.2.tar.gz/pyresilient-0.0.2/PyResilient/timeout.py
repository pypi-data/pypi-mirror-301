

from .handlers.timeout_handler import TimeoutHandler
import asyncio
import functools
from typing import Any, Callable
def timeout(timeout: int, exception: Exception = TimeoutError) -> Callable:


    
    """
    Decorator to enforce a timeout on a function. Raises the given exception if the timeout is exceeded.

    Args:
        timeout (int): The timeout duration in seconds.
        exception (Exception): The exception to raise if the timeout is exceeded.

    Returns:
        Callable: The decorated function.
    """

    def decorator(func: Callable) -> Callable:
        handler = TimeoutHandler(func, timeout, exception)
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def wrapped(*args: Any, **kwargs: Any) -> Any:
                return await handler(*args, **kwargs)

            return wrapped
        else:

            @functools.wraps(func)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                return handler(*args, **kwargs)

            return wrapped

    return decorator