# pylint: disable = W0212
import sys
from typing import Any, List, Set, Tuple


NEW_TYPING = sys.version_info[:3] >= (3, 7, 0)  # PEP 560


def _get_origin(tp):
    """Return x.__origin__ or type(x) based on the Python version."""
    if hasattr(tp, "_gorg"):
        return tp._gorg
    if getattr(tp, "__origin__", None) is not None:
        return tp.__origin__
    return tp


OLD_TYPE_ORIGINS = {List: list, Tuple: tuple, Set: set}


def get_origin(tp):
    origin = _get_origin(tp)
    if not NEW_TYPING and tp in OLD_TYPE_ORIGINS:
        return OLD_TYPE_ORIGINS[tp]
    return origin


def match_types(tp, *matches) -> bool:
    """Match the given type to list of other types.

    :param tp:
    :param matches:
    """
    return any([get_origin(m) is get_origin(tp) for m in matches])


ARGS = '__args__'


def unpack_type(tp, default=str) -> Any:
    """Unpack subscripted type.

    Args:
        tp:
        default:

    Returns:
        type inside the container type
    """
    if getattr(tp, ARGS, None) is not None:
        inner_tp = getattr(tp, ARGS)
        if match_types(tp, list):
            if str(inner_tp[0]) != '~T':
                return inner_tp[0]
        return inner_tp
    return default
