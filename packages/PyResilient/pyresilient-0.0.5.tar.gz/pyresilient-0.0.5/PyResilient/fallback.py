from typing import Any, Callable, Tuple, Type
import asyncio
import functools
from .handlers.fallback_handler import FallbackHandler


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