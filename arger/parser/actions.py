import argparse
from typing import Any, Tuple, Union

from ..types import UNDEFINED, VarArg, VarKw
from ..typing_utils import (
    cast,
    get_inner_args,
    get_origin,
    is_enum,
    is_iterable,
    is_tuple,
    unpack_type,
)


def get_nargs(typ: Any) -> Tuple[Any, Union[int, str]]:
    inner = unpack_type(typ)
    if (
        is_tuple(typ)
        and typ != tuple
        and not isinstance(typ, (VarKw, VarArg))
        and get_inner_args(typ)
    ):
        args = get_inner_args(typ)
        inner = inner if len(set(args)) == 1 else str
        return inner, '+' if (... in args) else len(args)
    return inner, "*"


class TypeAction(argparse.Action):
    """After the parse update the type of value"""

    def __init__(self, *args, **kwargs):
        typ = kwargs.pop("type", UNDEFINED)
        self.orig_type = typ
        if typ is not UNDEFINED:
            origin = get_origin(typ)
            if is_iterable(origin):
                origin, kwargs["nargs"] = get_nargs(typ)

            if is_enum(origin):
                kwargs.setdefault("choices", [e.name for e in origin])
                origin = str

            kwargs["type"] = origin
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if is_iterable(self.orig_type):
            items = getattr(namespace, self.dest, ()) or ()
            items = list(items)
            items.extend(values)
            vals = items
        else:
            vals = values
        setattr(namespace, self.dest, cast(self.orig_type, vals))


# class CommandAction(argparse._SubParsersAction):
#     def __call__(self, *args, **kwargs):
#         super(CommandAction, self).__call__(*args, **kwargs)
