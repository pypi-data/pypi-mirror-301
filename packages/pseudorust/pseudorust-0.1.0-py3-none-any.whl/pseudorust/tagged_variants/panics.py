__all__ = ["AnyErr", "Panic", "BadUnwrap"]

from typing import Generic, TypeVar

from ._variant import SENTINEL

Exc = TypeVar("Exc", bound=Exception)


class AnyErr(RuntimeError):
    """The default error when no error is given to an Err.. Does not inherit from Panic."""


class Panic(RuntimeError):
    """The error raised by a bad method call on a `Variant`."""


class _ExpectedPanic(Panic):
    """The base for the generated Panics raised."""

    def __init__(self, expected: object = SENTINEL, *args: object) -> None:
        if expected is not SENTINEL:
            expected = f"expected: {expected}"
            super().__init__(expected, *args)
        else:
            super().__init__(*args)


class BadUnwrap(Generic[Exc], _ExpectedPanic):
    """The error raised when `unwrap` is called on a non-`Ok` value.."""
