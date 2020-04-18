import sys
from argparse import ArgumentParser
from typing import Any, Callable, Dict, Optional

from arger.parser.classes import Option
from arger.structs import Command
from arger.types import F


def _add_args(parser, args: Dict[str, Option]):
    for _, arg in args.items():
        arg.add(parser)


def _cmd_prepare(parser, cmd: Command):
    cmd_parser = parser.add_parser(name=cmd.name, help=cmd.desc)
    _add_args(cmd_parser, cmd.args)
    return cmd_parser


CMD = "command"
CMD_TITLE = "commands"


def _add_parsers(parser: "Arger", cmd: Command):
    commands = list(cmd)
    if commands:
        subparser = parser.add_subparsers(
            title=CMD_TITLE,  # cmd.name
            dest=CMD,  # cmd.name,
            # action=CommandAction,
            # description=cmd.desc,
            # type=cmd.callback,
        )
        for _, sub in commands:
            cmd_parser = _cmd_prepare(subparser, sub)
            _add_parsers(cmd_parser, sub)  # recursively add any nested commands


class Arger(ArgumentParser):
    """Contains one function (parser) or more functions (subparsers)."""

    def __init__(self, fn: Optional[F] = None, **kwargs):
        self._command = Command(fn)
        if self._command.desc:
            kwargs.setdefault("description", self._command.desc)

        super().__init__(**kwargs)

        if fn:  # lazily add arguments
            _add_args(self, self._command.args)

    def run(self, *args, capture_sys=True) -> Any:
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
        kwargs = vars(self.parse_args(args))  # type: Dict[str, Any]

        return self._command.run(**kwargs)

    @classmethod
    def init(cls, **kwargs) -> Callable[[Callable], "Arger"]:
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
