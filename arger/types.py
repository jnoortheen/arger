from typing import Any, Callable, TypeVar


F = TypeVar('F', bound=Callable[..., Any])

UNDEFINED = object()
"""sometimes the value could be None. we need this to distinguish such values."""


class VarArg:
    """Represent variadic arguent."""

    container: Any = tuple

    def __init__(self, tp):
        self.type = tp

    def __call__(self, *args, **kwargs):
        return self.type(*args, **kwargs)

    def __repr__(self):
        tp = getattr(self.type, "__name__", self.type)
        return f'{self.__class__.__name__}[{tp}]'

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))


class VarKw(VarArg):
    """Represent variadic keyword argument."""

    container = dict
