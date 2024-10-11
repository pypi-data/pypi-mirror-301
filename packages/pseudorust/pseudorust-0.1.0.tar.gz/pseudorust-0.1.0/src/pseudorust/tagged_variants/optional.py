__all__ = ["Optional", "Some", "Null", "NullType"]

from typing import TYPE_CHECKING

from ._null import Null, NullType
from ._ok import Ok as Some
from ._variant import T

Optional = Some[T] | NullType

if TYPE_CHECKING:
    __option: Optional[None]

    __option = Some(None)
    __value = __option.unwrap()

    __option = Null
    __never = __option.unwrap()
