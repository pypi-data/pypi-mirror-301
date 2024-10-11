from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
Exc = TypeVar("Exc", bound=Exception)

SENTINEL = object()


class Variant(Generic[T], ABC):
    """A variant. Might contain a value."""

    @abstractmethod
    def unwrap(self, expect: object = SENTINEL) -> T: ...
