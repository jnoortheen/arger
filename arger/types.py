from typing import Any, Callable, Dict, NewType, Tuple, TypeVar


F = TypeVar('F', bound=Callable[..., Any])

UNDEFINED = object()
"""sometimes the value could be None. we need this to distinguish such values."""

VarArg = NewType('VarArg', Tuple)
KwArg = NewType('KwArg', Dict)
