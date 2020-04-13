# pylint: disable = W0622
import argparse
from collections import OrderedDict
from typing import Callable, Dict, Optional

from .parser import opterate
from .types import F


class Option:
    def __init__(
        self,
        type: Callable,
        default=None,
        flags: Optional[str] = None,
        help: Optional[str] = None,
        metavar: Optional[str] = None,
        required=False,
    ):
        """Represent optional arguments to the command.

        Tries to be compatible to `ArgumentParser.add_argument
        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument`_.

        :param flags: Either a name or a list of option strings, e.g. -f, --foo.
        :param default: The value produced if the argument is absent from the command line.
        :param type: The type to which the command-line argument should be converted.
        :param help: A brief description of what the argument does.
        :param metavar: A name for the argument in usage messages.
        :param required: Whether or not the command-line option may be omitted (optionals only).
        """

        #:param nargs: The number of command-line arguments that should be consumed.
        # nargs: to be generated from the type

        # action: Union[str, Type[argparse.Action]]
        #:param action: The basic type of action to be taken when this argument is encountered at the command line.

        #         :param dest: The name of the attribute to be added to the object returned by parse_args().

        #         :param const: A constant value required by some action and nargs selections.
        # will be covered by typehint and default value given

        #         :param choices: A container of the allowable values for the argument.
        # will covered by enum type
        self.type = type
        self.default = default
        self.flags = flags
        self.help = help
        self.metavar = metavar
        self.required = required

        # tmp
        p = argparse.ArgumentParser()
        p.add_argument()


class Argument(Option):
    """Represent positional argument that are required."""

    def __init__(
        self, type: Callable, help: Optional[str] = None, metavar: Optional[str] = None
    ):
        super().__init__(type, help=help, metavar=metavar, required=True)


class Command:
    def __init__(self, fn: Optional[F] = None):
        self._fn = fn  # only the root element may not have a function associated.
        self.name: Optional[str] = fn.__name__ if fn else None
        self.desc, self.args = opterate(self._fn) if fn else (None, [])
        self._sub: Dict[str, 'Command'] = OrderedDict()

    def is_valid(self) -> bool:
        return bool(self._fn or len(self._sub))

    def run(self, command: Optional[str] = None, **kwargs):
        args = set()
        for k in self.args:
            if 'dest' in k[1]:
                args.add(k[1]['dest'])
            else:
                args.add(k[0][0])
        root_kwargs = {k: v for k, v in kwargs.items() if k in args}
        cmd_kwargs = {k: v for k, v in kwargs.items() if k not in args}

        results = OrderedDict()
        if root_kwargs and self.name:
            results[self.name] = self(**root_kwargs)
        if command:
            results[command] = self._sub[command](**cmd_kwargs)
        return results

    def __call__(self, *args, **kwargs):
        if self._fn:
            return self._fn(*args, **kwargs)
        raise NotImplementedError("No function to dispatch")

    def add(self, func: F) -> 'Command':
        cmd = Command(func)
        if cmd.name in self._sub:
            raise KeyError(f"Already defined a command named {cmd.name}")
        self._sub[func.__name__] = cmd
        return cmd

    def __iter__(self):
        yield from self._sub.items()
