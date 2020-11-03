import argparse
from typing import Any, Tuple, Union

from .. import typing_utils as tp_utils


def get_nargs(typ: Any) -> Tuple[Any, Union[int, str]]:
    inner = tp_utils.unpack_type(typ)
    if (
        tp_utils.is_tuple(typ)
        and typ != tuple
        and not isinstance(typ, (tp_utils.VarKw, tp_utils.VarArg))
        and tp_utils.get_inner_args(typ)
    ):
        args = tp_utils.get_inner_args(typ)
        inner = inner if len(set(args)) == 1 else str
        return inner, '+' if (... in args) else len(args)
    return inner, "*"


class TypeAction(argparse.Action):
    """After the parse update the type of value"""

    def __init__(self, *args, **kwargs):
        typ = kwargs.pop("type", tp_utils.UNDEFINED)
        self.orig_type = typ
        if typ is not tp_utils.UNDEFINED:
            origin = tp_utils.get_origin(typ)
            if tp_utils.is_iterable(origin):
                origin, kwargs["nargs"] = get_nargs(typ)

            if tp_utils.is_enum(origin):
                kwargs.setdefault("choices", [e.name for e in origin])
                origin = str

            kwargs["type"] = origin
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if tp_utils.is_iterable(self.orig_type):
            items = getattr(namespace, self.dest, ()) or ()
            items = list(items)
            items.extend(values)
            vals = items
        else:
            vals = values
        setattr(namespace, self.dest, tp_utils.cast(self.orig_type, vals))
