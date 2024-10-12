import logging
import inspect
from functools import wraps
from typing import Callable, TypeVar, Any, cast
from random import randrange

# Configure logging (adjust as needed)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

F = TypeVar("F", bound=Callable[..., Any])


def logstep(
    message: str,
    level: int = logging.INFO,
    show_start: bool = True,
    show_start_args: bool = True,
    show_finish: bool = True,
    show_finish_results: bool = True,
) -> Callable[[F], F]:
    """
    Decorator to log the start and finish of function execution.

    Args:
        message (str): Custom message to include in logs.
        level (int): Logging level.
        show_start (bool): Whether to log the start of the function.
        show_finish (bool): Whether to log the finish of the function.

    Returns:
        Callable: The decorated function with logging.
    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def awrapper(*args, **kwargs) -> Any:
                id = randrange(1, 100_000_000_000)
                try:
                    if show_start:
                        logging.log(
                            level,
                            f"{message} - Starting({id}) *{func.__name__}* with args: {args if show_start_args else ''}, kwargs: {kwargs}",
                        )

                    result = await func(*args, **kwargs)

                    if show_finish:
                        logging.log(
                            level,
                            f"{message} - Finished({id}) *{func.__name__}* with result: {result if show_finish_results else ''}",
                        )
                    return result
                except Exception as e:
                    logging.exception(
                        f"{message} - Exception({id}) *{func.__name__}* raised an exception: {e}"
                    )
                    raise  # Re-raise the exception after logging

            return cast(F, awrapper)
        else:

            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                id = randrange(1, 100_000_000_000)
                try:
                    if show_start:
                        logging.log(
                            level,
                            f"{message} - Starting({id}) *{func.__name__}* with args: {args if show_start_args else ''}, kwargs: {kwargs}",
                        )

                    result = func(*args, **kwargs)

                    if show_finish:
                        logging.log(
                            level,
                            f"{message} - Finished({id}) *{func.__name__}* with result: {result if show_finish_results else ''}",
                        )
                    return result
                except Exception as e:
                    logging.exception(
                        f"{message} - Exception({id}) *{func.__name__}* raised an exception: {e}"
                    )
                    raise

            return cast(F, wrapper)

    return decorator
