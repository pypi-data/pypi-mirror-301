"""Utils functions."""

import asyncio
import pickle  # nosec B403
from functools import wraps
from hashlib import md5
from inspect import isawaitable
from itertools import chain
from typing import Any, Optional

import nest_asyncio

from .types import Decorator, Func, KeyGenerator, Manipulator


def default_keygen(typed: bool, func: Func, *args: Any, **kwargs: Any) -> str:
    """
    Build a key to a function.

    Parameters
    ----------
    typed : bool
        If typed is set to true, function arguments of different types
        will be cached separately.
    func : Func
        Function.
    *args : Any
        Function positional arguments.
    **kwargs : Any
        Named function arguments.

    Returns
    -------
    str
        Cache identifier key.
    """
    hashable_args: tuple[Any, ...] = (
        (func.__module__, func.__name__),
        args,
        tuple(sorted(kwargs.items())),
    )
    if typed:
        hashable_args += tuple(
            type(value) for value in chain(args, sorted(kwargs.values()))
        )
    return md5(pickle.dumps(hashable_args)).hexdigest()  # nosec B324


async def make_key(
    namespace: str,
    keygen: Optional[KeyGenerator],
    typed: bool,
    func: Func,
    *args,
    **kwargs,
) -> str:
    """
    Make a key to a function.

    Parameters
    ----------
    namespace : str
        Namespace to cache.
    keygen : KeyGenerator, optional
        Function to generate a cache identifier key.
    typed : bool
        If typed is set to true, function arguments of different types
        will be cached separately.
    func : Func
        Function.
    *args : Any
        Function positional arguments.
    **kwargs : Any
        Named function arguments.

    Returns
    -------
    str
        Cache identifier key with namespace.
    """
    key = await ensure_async(
        keygen or default_keygen, typed, func, *args, **kwargs
    )
    return f'{namespace}:{key}'


def decoder_name(obj: object) -> str:
    """
    Get a class name.

    Parameters
    ----------
    obj : object
        Object to get class name.

    Returns
    -------
    str
        Class name.
    """
    return obj.__class__.__name__.lower()


async def ensure_async(func: Func, *args: Any, **kwargs: Any) -> Any:
    """
    Wait a function that needs to be awaited.

    Parameters
    ----------
    func : Func
        Function.
    *args : Any
        Function positional arguments.
    **kwargs : Any
        Named function arguments.

    Returns
    -------
    Any
        Functions result.
    """
    result = func(*args, **kwargs)
    return await result if isawaitable(result) else result


def manipulate(manipulator: Manipulator) -> Decorator:
    """
    Decorate a function.

    Parameters
    ----------
    manipulator : Manipulator
        Function that will handle a decorated function.

    Returns
    -------
    Decorator
        Decorator function.
    """
    try:
        nest_asyncio.apply()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        nest_asyncio.apply(loop)

    def wrapper(func: Func) -> Func:
        async def _async(*args, **kwargs):
            return await manipulator(func, *args, **kwargs)

        def _sync(*args, **kwargs):
            return asyncio.run(
                ensure_async(manipulator, func, *args, **kwargs)
            )

        if asyncio.iscoroutinefunction(func):
            return wraps(func)(_async)
        return wraps(func)(_sync)

    return wrapper
