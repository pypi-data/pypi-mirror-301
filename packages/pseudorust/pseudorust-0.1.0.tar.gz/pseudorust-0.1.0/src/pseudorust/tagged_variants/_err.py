from collections.abc import Iterable
from typing import TYPE_CHECKING, Generic, cast, overload

from typing_extensions import Never, override

from ._variant import SENTINEL, Exc, Variant
from .panics import AnyErr, BadUnwrap

__all__ = ["Err"]


class Err(Generic[Exc], Variant[Never]):
    @overload
    def __init__(self: "Err[AnyErr]") -> None: ...

    @overload
    def __init__(self, error: Exc) -> None: ...

    @overload
    def __init__(self: "Err[AnyErr]", *, values: Iterable[object]) -> None: ...

    @overload
    def __init__(self: "Err[AnyErr]", *, values: object) -> None: ...

    def __init__(
        self, error: Exc | None = None, values: Iterable[object] | object = SENTINEL
    ) -> None:
        if error is not None:
            self.__exc = error
        elif values is SENTINEL:
            self.__exc = AnyErr()
        elif not isinstance(values, Iterable):
            self.__exc = AnyErr(values)
        else:
            values = cast(Iterable[object], values)
            self.__exc = AnyErr(*values)

    @override
    def unwrap(self, expect: object = SENTINEL) -> Never:
        raise BadUnwrap(expect) from self.__exc


if TYPE_CHECKING:
    # using the type checker to assert that `Err` is a concrete implementation of `Variant`
    _ = Err(RuntimeError(612))
