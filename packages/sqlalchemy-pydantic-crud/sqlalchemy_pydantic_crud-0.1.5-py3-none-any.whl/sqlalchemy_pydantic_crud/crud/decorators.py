import asyncio
import functools
import logging
from functools import wraps

import sqlalchemy

from ..exceptions.crud import RepositoryIntegrityError
from ..interface.crud import BaseCrudInterface

logger = logging.getLogger(__name__)

def session_manager(func):
    """Декоратор, менеджер сессий - проверяет поле session в kwargs
    и если его нет или значение поля None - открывает сессию, обновляет kwargs
    Args:
        func: имя функции
    Returns:
        декоратор
    """

    @wraps(func)
    async def inner(*args, **kwargs):
        if "session" not in kwargs or kwargs["session"] is None:
            self_: BaseCrudInterface = args[0]
            try:
                async with self_.session_provider.session() as session, session.begin():
                    kwargs["session"] = session
                    result = await func(*args, **kwargs)
            except sqlalchemy.exc.IntegrityError:
                raise RepositoryIntegrityError
        else:
            result = await func(*args, **kwargs)
        return result

    return inner




def autologger(_logger=None, exception_only: bool = True):
    """
    Декоратор для логирования вызовов функции.
    """

    def decorator(func):
        def _log_func_call(bound_logger, func, *args, **kwargs) -> None:
            bound_logger.info(
                f"CALL {func.__name__} {args=} {kwargs=}",
            )

        def _log_func_complete(bound_logger, func, result) -> None:
            bound_logger.info(
                f"COMPLETED {func.__name__} with {result=}",
            )

        def _log_func_error(bound_logger, func, e, *args, **kwargs) -> None:
            bound_logger.exception(
                f"exception {type(e)} - {str(e)}, {args=} {kwargs=}",
            )

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            bound_logger = _logger or logger
            if not exception_only:
                _log_func_call(bound_logger, func, *args, **kwargs)
            try:
                result = func(*args, **kwargs)
                if not exception_only:
                    _log_func_complete(bound_logger, func, result)
                return result
            except Exception as e:
                _log_func_error(bound_logger, func, e, *args, **kwargs)
                raise

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            bound_logger = _logger or logger
            if not exception_only:
                _log_func_call(bound_logger, func, *args, **kwargs)
            try:
                result = await func(*args, **kwargs)
                if not exception_only:
                    _log_func_complete(bound_logger, func, result)
                return result
            except Exception as e:
                _log_func_error(bound_logger, func, e, *args, **kwargs)
                raise e

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator