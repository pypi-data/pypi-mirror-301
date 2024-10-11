from typing import overload

from .protocols import SupportsName

__all__ = ["name"]


@overload
def name(obj: SupportsName) -> str:
    """Returns `obj.__name__`."""


@overload
def name(obj: object) -> str:
    """Returns `type(obj).__name__`."""


def name(obj: object) -> str:
    name: object = getattr(obj, "__name__", None)
    if isinstance(name, str):
        return name
    return type(obj).__name__
