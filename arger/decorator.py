from argparse import ArgumentParser
from typing import Any, Callable, Dict, Optional, TypeVar

from .parser import opterate


CMD = "commands"
F = TypeVar('F', bound=Callable[..., Any])


class Arger(ArgumentParser):
    """Contains one function (parser) or more functions (subparsers).
    Also a decorator to ease up the process of creating parser with its own options.

    Usage: see `tests/examples`_.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._funcs: Dict[str, Any] = {}  # registry

    def dispatch(self, *args):
        if not self._funcs:
            raise NotImplementedError("No function added.")

        kwargs = vars(self.parse_args(args))  # type: Dict[str, Any]
        if len(self._funcs) == 1:
            return self.first_func(**kwargs)

        func = self._funcs[kwargs[CMD]]
        return func(**kwargs)

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
