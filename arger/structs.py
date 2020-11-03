from argparse import Namespace
from collections import OrderedDict
from typing import Any, Dict, Optional

from .parser import parse_function
from .parser.funcs import ParsedFunc
from .types import VarArg
from .typing_utils import F


class Command:
    """Hold function <-> Parser and add any more function as subparsers."""

    def __init__(self, fn: Optional[F] = None):
        self._fn = fn  # only the root element may not have a function associated.
        self.name = fn.__name__ if fn else ""
        self.docs = parse_function(fn) if fn else ParsedFunc('', '', {})
        self._sub: Dict[str, "Command"] = OrderedDict()

    def is_valid(self) -> bool:
        return bool(self._fn or len(self._sub))

    def __repr__(self):
        return f'<Command: {self.name}'

    def add(self, func: F) -> "Command":
        cmd = Command(func)
        if cmd.name in self._sub:
            raise KeyError(f"Already defined a command named {cmd.name}")
        self._sub[func.__name__] = cmd
        return cmd

    def callback(self, ns: Namespace) -> Any:
        if self._fn:
            kwargs = {}
            args = []
            for arg_name, arg_type in self.docs.args.items():
                val = getattr(ns, arg_name)
                if isinstance(arg_type.kwargs.get('type'), VarArg):
                    args = val
                else:
                    kwargs[arg_name] = val

            return self._fn(*args, **kwargs)
        return None

    def __iter__(self):
        yield from self._sub.items()
