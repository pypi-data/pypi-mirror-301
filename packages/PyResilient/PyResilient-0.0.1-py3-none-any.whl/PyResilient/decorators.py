import asyncio
import functools
from typing import Any, Callable, Tuple, Type
from .handlers.fallback_handler import FallbackHandler
from .handlers.timeout_handler import TimeoutHandler

def fallback(
    fallback_func: Callable, exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """
    Decorator function to apply a fallback strategy to a function.

    Args:
        fallback_func (Callable): The fallback function.
        exceptions (Tuple[Type[Exception], ...], optional): Tuple of exceptions to catch. Defaults to (Exception,).

    Returns:
        Callable: The decorated function.
    """

    def decorator(func: Callable) -> Callable:
        handler = FallbackHandler(func, fallback_func, exceptions)
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

def timeout(timeout: int, exception: Exception) -> Callable:


    
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
