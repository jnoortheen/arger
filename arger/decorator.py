from argparse import ArgumentParser
from typing import Any, Callable, Dict, Optional, TypeVar

from .parser import opterate
from .types import F


class Arger(ArgumentParser):
    """Contains one function (parser) or more functions (subparsers).
    Also a decorator to ease up the process of creating parser with its own options.

    Usage: see `tests/examples`_.
    """

    def __init__(self, fn: F = None, **kwargs):
        self._fn = fn

        desc, add_args = self._add_fn(fn)
        if desc:
            kwargs.setdefault("description", desc)

        super().__init__(**kwargs)

        if add_args:
            add_args()

        self._funcs: Dict[str, Any] = {}  # registry

    def _add_fn(self, fn) -> (str, Optional[Callable]):
        if fn is not None:
            desc, args = opterate(fn)

            def add_args():  # lazy adding of arguments
                for flags, kw in args:
                    self.add_argument(*flags, **kw)

            return desc, add_args
        return "", None

    def run(self, *args):
        """The arguments will be passed onto self.parse_args and
        then the respective function will get called with parsed arguments."""
        if not self._funcs and not self._fn:
            raise NotImplementedError("No function to dispatch.")

        kwargs = vars(self.parse_args(args))  # type: Dict[str, Any]
        if self._fn is not None:
            return self._fn(**kwargs)

        # todo: implement
        # func = self._funcs[kwargs[CMD]]
        # return func(**kwargs)

    def __call__(self, func: F) -> F:
        """Decorator.

        called as a decorator to add any function as a command to the parser
        """
        self._funcs[func.__name__] = func
        return func

    def add_command(self, func: F) -> F:
        """Creates subparser and adds the function as one of the subcommand
        :param func:
        :return:
        """
        self._funcs[func.__name__] = func
        return func
