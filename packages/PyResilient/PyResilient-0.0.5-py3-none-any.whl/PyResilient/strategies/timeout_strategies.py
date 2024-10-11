import asyncio
from multiprocessing.pool import ThreadPool
from typing import Any, Callable, Dict, Tuple
from multiprocessing.context import TimeoutError


class TimeoutStrategy:
    """
    Strategy interface for handling function execution with a timeout.

    Methods:
        apply_timeout(func, args, kwargs, timeout, exception): Apply a timeout to the function execution.
    """

    def apply_timeout(
        self,
        func: Callable,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
        timeout: int,
        exception: Exception
    ) -> Any:
        raise NotImplementedError("This method should be overridden by subclasses")

class SyncTimeoutStrategy(TimeoutStrategy):
    """
    Concrete strategy for handling synchronous functions with a timeout.
    """

    def apply_timeout(
        self,
        func: Callable,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
        timeout: int,
        exception: Exception
    ) -> Any:
        try:
            pool = ThreadPool(processes=1)
            sync_result = pool.apply_async(func, args, kwargs)
            return sync_result.get(timeout)
        except Exception as e:
            excep = exception if isinstance(e, TimeoutError) else e
            raise excep

class AsyncTimeoutStrategy(TimeoutStrategy):
    """
    Concrete strategy for handling asynchronous functions with a timeout.
    """

    async def apply_timeout(
        self,
        func: Callable,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
        timeout: int,
        exception: Exception
    ) -> Any:
        try:
            return await asyncio.wait_for(func(*args, **kwargs), timeout)
        except Exception as e:
            excep = exception if isinstance(e, asyncio.TimeoutError) else e
            raise excep
