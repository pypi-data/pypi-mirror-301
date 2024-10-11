from functools import cached_property
from typing import Protocol

__all__ = ["SupportsNameAssignment", "SupportsNameProperty", "SupportsName"]


class SupportsNameAssignment(Protocol):
    """
    Any class which assigns `__name__` to a string.
    """

    __name__: str | cached_property[str]


class SupportsNameProperty(Protocol):
    """
    Any class which defines a `__name__` property.
    """

    @property
    def __name__(self) -> str: ...


SupportsName = SupportsNameAssignment | SupportsNameProperty
"""Any class which has an string accessor on `__name__`."""
