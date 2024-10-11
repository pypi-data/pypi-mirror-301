__all__ = ["Result", "Ok", "Err"]

from typing import TYPE_CHECKING, TypeAlias

from ._err import Err
from ._ok import Ok
from ._variant import Exc, T

Result: TypeAlias = Ok[T] | Err[Exc]

if TYPE_CHECKING:
    # using the type checker to assert that `Ok` is a concrete implementation of `Variant`

    from .panics import AnyErr

    __Result = Result[tuple[()], AnyErr]

    __result: __Result = Ok(())
    __s: tuple[()] = __result.unwrap()

    __result = Err()
    __result.unwrap()

    print("unreachable!")  # pyright: ignore[reportUnreachable]
