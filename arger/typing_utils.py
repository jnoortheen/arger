# pylint: disable = W0212
import sys


NEW_TYPING = sys.version_info[:3] >= (3, 7, 0)  # PEP 560


def _origin(tp):
    """Return x.__origin__ or type(x) based on the Python version."""
    if hasattr(tp, "_gorg"):
        return tp._gorg
    if getattr(tp, "__origin__", None) is not None:
        return tp.__origin__
    return tp


def match_types(tp, *matches) -> bool:
    """Match the given type to list of other types.

    :param tp:
    :param matches:
    """
    return any([_origin(m) is _origin(tp) for m in matches])
