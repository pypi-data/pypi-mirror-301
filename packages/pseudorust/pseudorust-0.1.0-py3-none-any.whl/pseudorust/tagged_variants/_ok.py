from typing import TYPE_CHECKING

from typing_extensions import override

from ._variant import SENTINEL, T, Variant

__all__ = ["Ok"]


class Ok(Variant[T]):
    def __init__(self, value: T) -> None:
        self.__value = value

    @override
    def unwrap(self, expect: object = SENTINEL) -> T:
        return self.__value


if TYPE_CHECKING:
    # using the type checker to assert that `Ok` is a concrete implementation of `Variant`
    _ = Ok(413)
