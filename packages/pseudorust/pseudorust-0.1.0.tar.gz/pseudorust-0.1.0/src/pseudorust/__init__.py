"""All the types I don't want to implement twice."""

__all__ = [
    # dunder_functions
    "name",
    # info
    "__author__",
    "__copyright__",
    "__credits__",
    "__license__",
    "__maintainer__",
    "__version__",
    # protocols
    "SupportsNameAssignment",
    "SupportsNameProperty",
    "SupportsName",
    # tagged_variants
    "AnyErr",
    "BadUnwrap",
    "Err",
    "Null",
    "NullType",
    "Ok",
    "Optional",
    "Panic",
    "Result",
    "Some",
]


from .dunder_functions import name
from .info import (
    __author__,
    __copyright__,
    __credits__,
    __license__,
    __maintainer__,
    __version__,
)
from .protocols import SupportsName, SupportsNameAssignment, SupportsNameProperty
from .tagged_variants import (
    AnyErr,
    BadUnwrap,
    Err,
    Null,
    NullType,
    Ok,
    Optional,
    Panic,
    Result,
    Some,
)
