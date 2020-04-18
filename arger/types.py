from typing import Any, Callable, TypeVar


F = TypeVar("F", bound=Callable[..., Any])  # decorator


class _Undefined:
    """sometimes the value could be None. we need this to distinguish such values."""

    def __repr__(self):
        return 'UNDEFINED'


UNDEFINED = _Undefined()  # singleton


class VarArg:
    """Represent variadic arguent."""

    __origin__: Any = tuple
    __args__: Any = ()

    def __init__(self, tp):
        self.__args__ = (tp, ...)

    def __repr__(self):
        tp = self.__args__[0]
        tp = getattr(tp, "__name__", tp)
        return f"{self.__class__.__name__}[{tp}]"

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))


class VarKw(VarArg):
    """Represent variadic keyword argument."""

    __original__ = dict
