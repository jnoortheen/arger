from argparse import Action
from enum import Enum
from typing import Annotated, Literal

import arger

# following function parameters are added to the parser using type hints
# all positional parameters are converted to arguments
# while the keyword arguments become flags


class Num(Enum):
    ONE = 1
    TWO = 2


class ActionSubCls(Action):
    """custom action"""

    def __call__(self, parser, namespace, value, option_string=None):
        setattr(namespace, self.dest, value)


def function(
    # -> add_argument(dest='a', type=str)
    a_st: str,
    # -> add_argument(dest='a', type=int)
    a_in: int,
    # : one or more
    # -> add_argument(dest='a', type=int, nargs='+')
    a_tp: tuple[int, ...],
    # : consumes 2 positional arguments
    # -> add_argument(dest='a', type=int, nargs='2')
    a_tp_int: tuple[int, int],
    # : zero or more
    # -> add_argument(dest="a", type=int, nargs="*")
    a_ls: list[int],
    # : zero or one positional
    # -> add_argument(dest="a", type=int, nargs="?")
    a_opt: int | None,
    # : accepts str from cli and returns as an Enum.
    # -> add_argument(dest="a", choices=list(Num), type=lambda x: Num[x])
    a_en: Num,
    # : accepts str from cli and returns the same
    # -> add_argment(dest="a_lt", choices=["one", "two"], type=str)
    a_lt: Literal["one", "two"],
    # : custom arguments to the `Argument` can be delegated with `Annotated`
    # -> add_argument(dest="a", metavar="INT", type=int, action=ActionSubCls)
    a_cs: Annotated[
        int,
        arger.Argument(metavar="INT", action=ActionSubCls),
    ],
    # any optionals are converted to flags with default values
    # -> add_argument("--kwarg", "-k", dest="kwarg", type=int, default=0)
    kwarg: int = 0,
): ...
