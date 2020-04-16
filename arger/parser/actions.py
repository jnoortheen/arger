import argparse
from enum import Enum
from inspect import isclass

from ..types import UNDEFINED, VarArg, VarKw
from ..typing_utils import get_origin


class TypeAction(argparse.Action):
    """after the parse update the type of value"""

    def __init__(self, *args, **kwargs):
        typ = kwargs.pop("type", UNDEFINED)
        if typ is not UNDEFINED:
            typ = get_origin(typ)

            if typ in {list, tuple} or isinstance(typ, (VarArg, VarKw)):
                kwargs['nargs'] = '*'

            if isclass(typ) and issubclass(typ, Enum):
                kwargs.setdefault("choices", [e.name for e in typ])

            kwargs['type'] = typ
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        #     def __call__(self, parser, namespace, values, option_string=None):
        #         items = getattr(namespace, self.dest, None)
        #         items = _copy_items(items)
        #         items.append(self.const)
        #         setattr(namespace, self.dest, items)
        setattr(namespace, self.dest, values)


# class CommandAction(argparse._SubParsersAction):
#     def __call__(self, *args, **kwargs):
#         super(CommandAction, self).__call__(*args, **kwargs)
