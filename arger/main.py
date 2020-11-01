# pylint: disable = W0212 ; protected member

import argparse as ap
import copy
import sys
import typing as tp

from .structs import Command
from .types import F

CMD_TITLE = "commands"
LEVEL = '__level__'
FUNC_PREFIX = '_func_'
NS_PREFIX = '_namespace_'


def _add_args(parser, cmd: Command, level: int):
    parser.set_defaults(**{f'{FUNC_PREFIX}{level}': cmd.callback, LEVEL: level})
    for arg_name, arg in cmd.docs.args.items():
        if arg_name.startswith('_'):
            continue
        arg.add(parser)


def _cmd_prepare(
    parser: ap._SubParsersAction, cmd: Command, level: int
) -> ap.ArgumentParser:
    cmd_parser = parser.add_parser(
        name=cmd.name, help=cmd.docs.description if cmd.docs else ''
    )
    _add_args(cmd_parser, cmd, level)
    return cmd_parser


def _add_parsers(parser: tp.Union["Arger", ap.ArgumentParser], cmd: Command):
    commands = list(cmd)
    if commands:
        subparser = parser.add_subparsers(
            # action=CommandAction,
            title=CMD_TITLE,
        )
        for _, sub in commands:
            level = (parser.get_default(LEVEL) or 0) + 1
            cmd_parser = _cmd_prepare(subparser, sub, level=level)
            _add_parsers(cmd_parser, sub)  # recursively add any nested commands


class Arger(ap.ArgumentParser):
    """Contains one function (parser) or more functions (subparsers)."""

    def __init__(self, fn: tp.Optional[F] = None, **kwargs):
        kwargs.setdefault('formatter_class', ap.ArgumentDefaultsHelpFormatter)
        self._command = Command(fn)
        if self._command.docs.description:
            kwargs.setdefault("description", self._command.docs.description)

        super().__init__(**kwargs)

        if fn:  # lazily add arguments
            _add_args(self, self._command, level=0)

    def run(self, *args: str, capture_sys=True) -> ap.Namespace:
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
        namespace = self.parse_args(args)
        kwargs = vars(namespace)
        kwargs[NS_PREFIX] = copy.copy(namespace)
        # dispatch all functions as in hierarchy
        for level in range(kwargs.get(LEVEL, 0) + 1):
            func_name = f'{FUNC_PREFIX}{level}'
            if func_name in kwargs:
                kwargs[func_name](namespace)

        return namespace

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
