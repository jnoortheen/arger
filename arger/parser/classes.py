import argparse
from typing import Any, List, Optional

from arger.parser.utils import generate_flags

from ..types import UNDEFINED
from .actions import TypeAction


def get_action(
    _type, default=None,
):
    if default is False:
        return "store_true"
    if default is True:
        return "store_false"
    return TypeAction


class Option:
    def __init__(
        self, flags: Optional[List[str]] = None, default: Any = UNDEFINED, **kwargs,
    ):
        """Represent optional arguments to the command.

        Tries to be compatible to `ArgumentParser.add_argument
        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument`_.

        :param flags: Either a name or a list of option strings, e.g. -f, --foo.
        :param default: The value produced if the argument is absent from the command line.
            * The default value assigned to a keyword argument helps determine
                the type of option and action.
            * The default value is assigned directly to the parser's default for that option.

            * In addition, it determines the ArgumentParser action
                * a default value of False implies store_true, while True implies store_false.
                * If the default value is a list, the action is append
                (multiple instances of that option are permitted).
                * Strings or None imply a store action.
        :param type: The type to which the command-line argument should be converted.
        :param help: A brief description of what the argument does.
        :param metavar: A name for the argument in usage messages.
        :param required: Whether or not the command-line option may be omitted (optionals only).
        :param kwargs: will be passed onto parser.add_argument

        :param nargs: The number of command-line arguments that should be consumed. nargs: to be generated from the type
        :param dest: The name of the attribute to be added to the object returned by parse_args().
        :param const: covered by type-hint and default value given
        :param choices: covered by enum type

        :param action: The basic type of action to be taken when this argument is encountered at the command line.
        :type action: Union[str, Type[argparse.Action]]
        """
        name = kwargs.pop('name', None)
        self.flags = flags or ([name] if name else [])

        tp = kwargs.pop('type', UNDEFINED)
        if default is not UNDEFINED:
            kwargs["default"] = default

            if tp is UNDEFINED and default is not None:
                tp = type(default)

        action = get_action(tp, default)
        kwargs.setdefault('action', action)
        if tp is not UNDEFINED and action not in {  # bool actions dont need type
            'store_false',
            'store_true',
        }:
            kwargs['type'] = tp

        self.kwargs = kwargs

    def add(self, parser: argparse.ArgumentParser):
        return parser.add_argument(*self.flags, **self.kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.flags}, {repr(self.kwargs)}'

    def set_flags(self, option_generator, name: str):
        hlp = self.kwargs.pop('help').split()
        # generate flags
        self.flags = generate_flags(name, hlp, option_generator)
        self.kwargs['help'] = " ".join(hlp)


class Argument(Option):
    """Represent positional argument that are required."""
