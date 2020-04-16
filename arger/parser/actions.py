import argparse
from enum import Enum
from inspect import isclass
from typing import Any, List, Tuple, Union

from ..types import UNDEFINED, VarArg, VarKw
from ..typing_utils import ARGS, get_origin, match_types, unpack_type


def get_nargs(typ: Any) -> Union[int, str]:
    if match_types(typ, Tuple) and hasattr(typ, ARGS) and getattr(typ, ARGS):
        args = getattr(typ, ARGS)
        return '+' if (... in args) else len(args)
    return "*"


class TypeAction(argparse.Action):
    """after the parse update the type of value"""

    def __init__(self, *args, **kwargs):
        typ = kwargs.pop("type", UNDEFINED)
        self.container_type = None
        if typ is not UNDEFINED:
            origin = get_origin(typ)

            if origin in {list, tuple} or isinstance(origin, (VarArg, VarKw)):
                kwargs["nargs"] = get_nargs(typ)
                inner_type = unpack_type(typ)
                if match_types(typ, list):
                    origin = inner_type
                else:  # tuple
                    origin = str
                self.container_type = typ
            if isclass(origin) and issubclass(origin, Enum):
                kwargs.setdefault("choices", [e.name for e in typ])

            kwargs["type"] = origin
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        #     def __call__(self, parser, namespace, values, option_string=None):
        #         items = getattr(namespace, self.dest, None)
        #         items = _copy_items(items)
        #         items.append(self.const)
        #         setattr(namespace, self.dest, items)
        if self.container_type and match_types(self.container_type, tuple):
            values = tuple(values)
        setattr(namespace, self.dest, values)


# class CommandAction(argparse._SubParsersAction):
#     def __call__(self, *args, **kwargs):
#         super(CommandAction, self).__call__(*args, **kwargs)
