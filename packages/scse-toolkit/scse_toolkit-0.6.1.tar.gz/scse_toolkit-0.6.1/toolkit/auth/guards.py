import functools
import re
from typing import Callable, cast

import polars as pl

from toolkit.exceptions import Forbidden
from toolkit.manager.models import AccessType, Ixmp4Instance

from .context import AuthorizationContext


def raise_or_return(func: Callable[..., bool]):
    """Decorator which adds an optional keyword argument `raise_exc` to the decorated function.
    If `raise_exc` is `True` or an exception or exception class, the/ an exception will be raised if the function returns a 'falsy' value.
    By default the raised exception is `Forbidden`."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> bool:
        raise_or_exc: bool | type[Exception] | Exception = kwargs.pop(
            "raise_exc", False
        )

        is_exc = False
        if isinstance(raise_or_exc, Exception):
            is_exc = True

        if isinstance(raise_or_exc, type) and issubclass(raise_or_exc, Exception):
            is_exc = True

        is_valid = isinstance(raise_or_exc, bool) or is_exc

        if not is_valid:
            raise ValueError("Named argument 'raise' must be `bool` or `Exception`.")

        exc: Exception = Forbidden()
        if raise_or_exc and is_exc:
            exc = cast(Exception, raise_or_exc)

        result = func(*args, **kwargs)
        if raise_or_exc and not result:
            raise exc
        else:
            return result

    return wrapper


def has_permission(
    platform: Ixmp4Instance,
    acceptable_access_types: list[AccessType],
    models: list[str] | None = None,
):
    ctx = AuthorizationContext.get_current_context()
    if ctx is None:
        return False

    if ctx.user is not None:
        if ctx.user.is_superuser:
            return True
        if platform.management_group in ctx.user.groups:
            return True

    df = ctx.tabulate_permissions(platform)
    if df.is_empty():
        return False

    df = df.filter(
        pl.col("access_type").is_in([str(aat) for aat in acceptable_access_types])
    )

    if models is not None:
        regex = re.compile("^" + "|".join(df["regex"]) + "$")
        for model in models:
            if regex.match(model) is None:
                return False

    return not df.is_empty()


@raise_or_return
def has_edit_permission(platform: Ixmp4Instance, models: list[str] | None = None):
    return has_permission(platform, [AccessType.EDIT], models=models)


@raise_or_return
def has_submit_permission(platform: Ixmp4Instance, models: list[str] | None = None):
    return has_permission(platform, [AccessType.EDIT, AccessType.SUBMIT], models=models)


@raise_or_return
def has_view_permission(platform: Ixmp4Instance, models: list[str] | None = None):
    return has_permission(
        platform, [AccessType.EDIT, AccessType.SUBMIT, AccessType.VIEW], models=models
    )


@raise_or_return
def is_verified():
    ctx = AuthorizationContext.get_current_context()
    if ctx is None:
        return False
    if ctx.user is None:
        return False
    return ctx.user.is_verified


@raise_or_return
def is_authenticated():
    ctx = AuthorizationContext.get_current_context()
    if ctx is None:
        return False
    if ctx.user is None:
        return False
    return ctx.user.is_authenticated


@raise_or_return
def is_staff():
    if not is_authenticated():
        return False
    ctx = AuthorizationContext.get_current_context()
    return ctx.user.is_staff


@raise_or_return
def is_superuser():
    if not is_authenticated():
        return False
    ctx = AuthorizationContext.get_current_context()
    return ctx.user.is_superuser
