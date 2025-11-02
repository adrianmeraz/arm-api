from functools import wraps

from fastapi import HTTPException

from src import logs
from src.amazon import param_store

logger = logs.get_logger()


def require_dev_environment(func):
    """Decorator to restrict access to handlers when ENVIRONMENT != 'dev'.

    When applied to an endpoint handler (or any callable used by FastAPI),
    this decorator reads the `ENVIRONMENT` value from the parameter store and
    raises HTTPException(status_code=403) if the environment is not 'dev'.

    Usage:
        from src.auth.authorizer import require_dev_environment

        @router.post("/...")
        @require_dev_environment
        def create(...):
            ...

    The decorator logs a warning when blocking access.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        env = param_store.get_secret('ENVIRONMENT')
        if env != 'dev':
            logger.warning(f'Blocked call to {func.__name__} in non-dev environment: {env}')
            raise HTTPException(status_code=403, detail="Not Authorized")
        return func(*args, **kwargs)

    return wrapper
