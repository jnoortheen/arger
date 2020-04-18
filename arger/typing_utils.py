# pylint: disable = W0212
import sys
from enum import Enum
from inspect import isclass
from typing import Any, FrozenSet, List, Set, Tuple


NEW_TYPING = sys.version_info[:3] >= (3, 7, 0)  # PEP 560


def _get_origin(tp):
    """Return x.__origin__ or type(x) based on the Python version."""
    if hasattr(tp, "_gorg"):
        return tp._gorg
    if getattr(tp, "__origin__", None) is not None:
        return tp.__origin__
    return tp


def define_old_types():
    origins = {}
    if not NEW_TYPING:
        for tp, orig in {
            List: list,
            Tuple: tuple,
            Set: set,
            FrozenSet: frozenset,
        }.items():
            if hasattr(tp, '__name__'):
                origins[tp.__name__] = orig  # type: ignore
    return origins


OLD_TYPE_ORIGINS = define_old_types()


def get_origin(tp):
    origin = _get_origin(tp)
    if not NEW_TYPING and hasattr(tp, '__name__') and tp.__name__ in OLD_TYPE_ORIGINS:
        return OLD_TYPE_ORIGINS[tp.__name__]
    return origin


def match_types(tp, *matches) -> bool:
    """Match the given type to list of other types.

    :param tp:
    :param matches:
    """
    return any([get_origin(m) is get_origin(tp) for m in matches])


ARGS = '__args__'


def get_inner_args(tp):
    return getattr(tp, ARGS, ())


def unpack_type(tp, default=str) -> Any:
    """Unpack subscripted type for use with argparser.

    Args:
        tp:
        default:

    Returns:
        type inside the container type
    """
    if get_inner_args(tp):
        inner_tp = getattr(tp, ARGS)
        if inner_tp and str(inner_tp[0]) not in {'~T', 'typing.Any'}:
            return inner_tp[0]
    return default


def is_iterable(tp):
    origin = get_origin(tp)
    return origin in {list, tuple, set, frozenset}


def is_enum(tp):
    return isclass(tp) and issubclass(tp, Enum)


def is_tuple(tp):
    return match_types(tp, tuple)


def cast(tp, val) -> Any:
    origin = get_origin(tp)

    if is_enum(origin):
        return origin[val]

    if is_iterable(origin):
        val = origin(val)
        args = get_inner_args(tp)
        if origin in {tuple,} and args and Ellipsis not in args:
            return tuple(cast(args[idx], v) for idx, v in enumerate(val))
        return origin([cast(unpack_type(tp), v) for v in val])

    return origin(val)
