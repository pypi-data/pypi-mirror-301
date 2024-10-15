"""Types implemetations."""

from sys import version_info
from typing import Any, Awaitable, Callable, TypedDict, TypeVar, Union

if version_info < (3, 10):  # pragma: no cover
    from typing_extensions import Concatenate, ParamSpec, TypeAlias
else:
    from typing import Concatenate, ParamSpec, TypeAlias  # type: ignore

T = TypeVar('T')
P = ParamSpec('P')

Func: TypeAlias = Callable[P, Union[Awaitable[T], T]]
Decorator: TypeAlias = Callable[[Func], Func]
KeyGenerator: TypeAlias = Callable[
    Concatenate[bool, Func, P], Union[Awaitable[str], str]
]
AsyncKeyGenerator: TypeAlias = Callable[Concatenate[Func, P], Awaitable[str]]

Manipulator: TypeAlias = Callable[
    Concatenate[Any, Func, P], Union[Awaitable[T], T]
]
Encoder: TypeAlias = Callable[[Any], Any]
Decoder: TypeAlias = Callable[[Any], Any]


class Encoded(TypedDict):
    """Encoded type."""

    __val: Any
    __decoder: str
