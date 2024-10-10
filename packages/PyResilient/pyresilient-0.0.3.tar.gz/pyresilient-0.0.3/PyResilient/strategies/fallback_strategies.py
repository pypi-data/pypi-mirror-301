import asyncio
import inspect
from typing import Any, Callable, Dict, Tuple

class FallbackStrategy:
    """
    Strategy interface for handling function execution with a fallback.

    Methods:
        map_args(func, fallback_func, args, kwargs): Maps arguments from the original function
                                                     to the fallback function.
    """

    def map_args(
        self,
        func: Callable,
        fallback_func: Callable,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ) -> Tuple[list, Dict[str, Any]]:
        """
        Map the arguments from the original function to the fallback function.

        Args:
            func (Callable): The original function.
            fallback_func (Callable): The fallback function.
            args (Tuple[Any, ...]): Positional arguments for the original function.
            kwargs (Dict[str, Any]): Keyword arguments for the original function.

        Returns:
            Tuple[list, Dict[str, Any]]: Mapped positional and keyword arguments for the fallback function.
        """
        func_signature = inspect.signature(func)
        fallback_signature = inspect.signature(fallback_func)
        func_params = list(func_signature.parameters.keys())
        fallback_params = fallback_signature.parameters

        fallback_args = []
        fallback_kwargs = {}

        for param_name in fallback_params:
            if param_name in func_params:
                index = func_params.index(param_name)
                if index < len(args):
                    fallback_args.append(args[index])
                elif param_name in kwargs:
                    fallback_kwargs[param_name] = kwargs[param_name]

        return fallback_args, fallback_kwargs


class SyncFallbackStrategy(FallbackStrategy):
    """
    Concrete strategy for handling synchronous functions.

    Methods:
        handle(func, fallback_func, args, kwargs): Executes the original function and falls back if an exception occurs.
    """

    def handle(
        self,
        func: Callable,
        fallback_func: Callable,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ) -> Any:
        """
        Execute the original function and fall back to the fallback function if an exception occurs.

        Args:
            func (Callable): The original function.
            fallback_func (Callable): The fallback function.
            args (Tuple[Any, ...]): Positional arguments for the original function.
            kwargs (Dict[str, Any]): Keyword arguments for the original function.

        Returns:
            Any: Result of the original or fallback function.
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            fallback_args, fallback_kwargs = self.map_args(func, fallback_func, args, kwargs)
            if asyncio.iscoroutinefunction(fallback_func):
                loop = asyncio.get_event_loop()
                return loop.run_until_complete(fallback_func(*fallback_args, **fallback_kwargs))
            else:
                return fallback_func(*fallback_args, **fallback_kwargs)


class AsyncFallbackStrategy(FallbackStrategy):
    """
    Concrete strategy for handling asynchronous functions.

    Methods:
        handle(func, fallback_func, args, kwargs): Executes the original async function and falls back if an exception occurs.
    """

    async def handle(
        self,
        func: Callable,
        fallback_func: Callable,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ) -> Any:
        """
        Execute the original async function and fall back to the fallback function if an exception occurs.

        Args:
            func (Callable): The original async function.
            fallback_func (Callable): The fallback function.
            args (Tuple[Any, ...]): Positional arguments for the original function.
            kwargs (Dict[str, Any]): Keyword arguments for the original function.

        Returns:
            Any: Result of the original or fallback function.
        """
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            fallback_args, fallback_kwargs = self.map_args(func, fallback_func, args, kwargs)
            if asyncio.iscoroutinefunction(fallback_func):
                return await fallback_func(*fallback_args, **fallback_kwargs)
            else:
                return fallback_func(*fallback_args, **fallback_kwargs)
