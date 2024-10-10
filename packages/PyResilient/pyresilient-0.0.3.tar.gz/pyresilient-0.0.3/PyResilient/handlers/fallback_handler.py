import asyncio
from typing import Any, Callable, Tuple, Type
from ..strategies.fallback_strategies import SyncFallbackStrategy, AsyncFallbackStrategy
from .base_handler import BaseHandler


class FallbackHandler(BaseHandler):
    """
    Context class that uses a fallback strategy to handle function execution.

    Attributes:
        func (Callable): The original function.
        fallback_func (Callable): The fallback function.
        exceptions (Tuple[Type[Exception], ...]): Tuple of exceptions to catch.
        strategy (FallbackStrategy): Strategy for handling function execution.
    """

    def __init__(
        self,
        func: Callable,
        fallback_func: Callable,
        exceptions: Tuple[Type[Exception], ...],
    ):
        """
        Initialize the FallbackHandler with the given function, fallback function, and exceptions.

        Args:
            func (Callable): The original function.
            fallback_func (Callable): The fallback function.
            exceptions (Tuple[Type[Exception], ...]): Tuple of exceptions to catch.
        """
        self.func = func
        self.fallback_func = fallback_func
        self.exceptions = exceptions
        self.strategy = (
            AsyncFallbackStrategy()
            if asyncio.iscoroutinefunction(func)
            else SyncFallbackStrategy()
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the original function and fall back if an exception occurs.

        Args:
            args (Any): Positional arguments for the original function.
            kwargs (Any): Keyword arguments for the original function.

        Returns:
            Any: Result of the original or fallback function.
        """
        if asyncio.iscoroutinefunction(self.func):

            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await self.strategy.handle(
                    self.func, self.fallback_func, args, kwargs
                )

            return async_wrapper(*args, **kwargs)
        else:
            return self.strategy.handle(self.func, self.fallback_func, args, kwargs)
