import asyncio
from typing import Any, Callable
from ..strategies.timeout_strategies import SyncTimeoutStrategy, AsyncTimeoutStrategy
from .base_handler import BaseHandler


class TimeoutHandler(BaseHandler):
    """
    Context class that uses a timeout strategy to handle function execution.

    Attributes:
        func (Callable): The original function.
        timeout (int): The timeout duration in seconds.
        exception (Exception): The exception to raise if the timeout is exceeded.
        strategy (TimeoutStrategy): Strategy for handling function execution with a timeout.
    """

    def __init__(
        self,
        func: Callable,
        timeout: int,
        exception: Exception,
    ):
        """
        Initialize the TimeoutHandler with the given function, timeout duration, and exception.

        Args:
            func (Callable): The original function.
            timeout (int): The timeout duration in seconds.
            exception (Exception): The exception to raise if the timeout is exceeded.
        """
        self.func = func
        self.timeout = timeout
        self.exception = exception
        self.strategy = (
            AsyncTimeoutStrategy()
            if asyncio.iscoroutinefunction(func)
            else SyncTimeoutStrategy()
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the original function with a timeout.

        Args:
            args (Any): Positional arguments for the original function.
            kwargs (Any): Keyword arguments for the original function.

        Returns:
            Any: Result of the original function or raises an exception if the timeout is exceeded.
        """
        if asyncio.iscoroutinefunction(self.func):

            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await self.strategy.apply_timeout(
                    self.func, args, kwargs, self.timeout, self.exception
                )

            return async_wrapper(*args, **kwargs)
        else:
            return self.strategy.apply_timeout(
                self.func, args, kwargs, self.timeout, self.exception
            )
