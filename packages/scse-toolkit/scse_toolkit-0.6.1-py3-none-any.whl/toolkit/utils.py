import functools
import time
from importlib import import_module
from typing import Any, Callable


def import_member(member_str: str) -> tuple[Any, tuple[str, str]]:
    module_name, member_name = member_str.rsplit(":", 1)
    module = import_module(module_name)
    obj: object | None = getattr(module, member_name, None)
    return obj, (member_name, module_name)


def ttl_cache(ttl_seconds: int = 60 * 15, **kwargs):
    """Caches a functions results for a fixed period of time using `functools.lru_cache`"""

    def decorator(func: Callable):
        def get_ttl_hash():
            """Return the same value withing `seconds` time period"""
            return round(time.time() / ttl_seconds)

        @functools.lru_cache(**kwargs)
        def ttl_func(*args, ttl_hash=None, **kwargs):
            del ttl_hash
            return func(*args, **kwargs)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> bool:
            return ttl_func(*args, ttl_hash=get_ttl_hash(), **kwargs)

        return wrapper

    return decorator
