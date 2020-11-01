# pylint: disable = W0212 ; protected member

import argparse as ap
import sys
import typing as tp

from .parser.classes import Argument
from .structs import Command
from .types import F


def _add_args(parser, args: tp.Dict[str, Argument]):
    for _, arg in args.items():
        arg.add(parser)


def _cmd_prepare(parser: ap._SubParsersAction, cmd: Command) -> ap.ArgumentParser:
    cmd_parser = parser.add_parser(
        name=cmd.name, help=cmd.docs.description if cmd.docs else ''
    )
    cmd_parser.set_defaults(func=cmd.callback)
    _add_args(cmd_parser, cmd.docs.args if cmd.docs else {})
    return cmd_parser


def _add_parsers(parser: tp.Union["Arger", ap.ArgumentParser], cmd: Command):
    commands = list(cmd)
    if commands:
        subparser = parser.add_subparsers(
            # action=CommandAction,
            # description=cmd.desc,
        )
        for _, sub in commands:
            cmd_parser = _cmd_prepare(subparser, sub)
            _add_parsers(cmd_parser, sub)  # recursively add any nested commands


class Arger(ap.ArgumentParser):
    """Contains one function (parser) or more functions (subparsers)."""

    def __init__(self, fn: tp.Optional[F] = None, **kwargs):
        self._command = Command(fn)
        if self._command.docs and self._command.docs.description:
            kwargs.setdefault("description", self._command.docs.description)

        super().__init__(**kwargs)

        if fn:  # lazily add arguments
            _add_args(self, self._command.docs.args)

    def run(self, *args, capture_sys=True) -> tp.Dict[str, tp.Any]:
        """Parse cli and dispatch functions.

        Args:
            *args: The arguments will be passed onto self.parse_args
        """
        if not self._command.is_valid():
            raise NotImplementedError("No function to dispatch.")

        # populate sub-parsers
        _add_parsers(self, self._command)

        if not args and capture_sys:
            args = tuple(sys.argv[1:])
        return vars(self.parse_args(args))

    @classmethod
    def init(cls, **kwargs) -> tp.Callable[[tp.Callable], "Arger"]:
        """Create parser from function as a decorator.

        Args:
            func: main function that has description and has sub-command level arguments
        """

        def _wrapper(fn):
            return cls(fn, **kwargs)

        return _wrapper

    def add_cmd(self, func: F) -> Command:
        """Decorate the function as a sub-command.

        Args:
            func: function
        """
        return self._command.add(func)
