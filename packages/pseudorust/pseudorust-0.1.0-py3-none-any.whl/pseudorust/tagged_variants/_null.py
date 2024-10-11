from typing_extensions import Never, override

from ._variant import SENTINEL, Variant
from .panics import BadUnwrap

__all__ = ["Null", "NullType"]


class NullType(Variant[Never]):
    @override
    def unwrap(self, expect: object = SENTINEL) -> Never:
        raise BadUnwrap(expect)


# null is stateless, so this is actually perfectly fine
Null = NullType()
