# pylint: disable = W0221
import argparse
import inspect
from typing import Any, Tuple

from arger.parser.utils import generate_flags

from ..types import UNDEFINED
from .actions import TypeAction


class Argument:
    """Represent positional argument that are required.

    Tries to be compatible to `ArgumentParser.add_argument
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument`_.
    """

    flags: Tuple[str, ...] = ()

    def __init__(
        self, **kwargs,
    ):
        """Represent optional arguments to the command.

        Args:
            type (Any): The type to which the command-line argument should be converted.
            help (str): A brief description of what the argument does.
            metavar (str): A name for the argument in usage messages.
            required (bool): Whether or not the command-line option may be omitted (optionals only).

            nargs (Union[int, str]): The number of command-line arguments that should be consumed.
                to be generated from the type-hint.
            dest (str): The name of the attribute to be added to the object returned by parse_args().
            const (Any): covered by type-hint and default value given
            choices (List[str]): covered by enum type
            action (Union[str, Type[argparse.Action]]): The basic type of action to be taken
                when this argument is encountered at the command line.
        """
        kwargs.setdefault('action', TypeAction)  # can be overridden by user
        self.kwargs = kwargs

    def add(self, parser: argparse.ArgumentParser):
        return parser.add_argument(*self.flags, **self.kwargs)

    @property
    def _kwargs_repr_(self):
        return {
            k: f"`{val.__name__}" if inspect.isclass(val) else val
            for k, val in self.kwargs.items()
        }

    def __repr__(self):
        """helps during tests"""
        return f"<{self.__class__.__name__}: {self.flags}, {repr(self.kwargs)}>"

    def update_flags(self, name: str):
        self.flags = (name,)

    def update(self, tp: Any = UNDEFINED, **_):
        """Update type externally."""
        tp = self.kwargs.pop('type', tp)
        if tp is not UNDEFINED:
            self.kwargs['type'] = tp


class Option(Argument):
    def __init__(self, *flags: str, **kwargs):
        """Represent optional arguments that has flags.

        Args:
            *flags: Either a name or a list of option strings, e.g. -f, --foo.
            default (Any): The value produced if the argument is absent from the command line.
                * The default value assigned to a keyword argument helps determine
                    the type of option and action.
                * The default value is assigned directly to the parser's default for that option.

                * In addition, it determines the ArgumentParser action
                    * a default value of False implies store_true, while True implies store_false.
                    * If the default value is a list, the action is append
                    (multiple instances of that option are permitted).
                    * Strings or None imply a store action.
        """
        super().__init__(**kwargs)
        self.flags = flags

    def update_flags(self, name: str, option_generator: Any = None):
        self.kwargs.setdefault('dest', name)
        if not self.flags and option_generator is not None:
            hlp = self.kwargs.pop("help").split()
            # generate flags
            self.flags = tuple(generate_flags(name, hlp, option_generator))
            self.kwargs["help"] = " ".join(hlp)

    def update(self, tp: Any = UNDEFINED, default: Any = UNDEFINED, **_):
        """Update type and default externally"""
        default = self.kwargs.pop('default', default)
        if default is not UNDEFINED:
            self.kwargs["default"] = default

            if isinstance(default, bool):
                self.kwargs['action'] = (
                    "store_true" if default is False else "store_false"
                )
                tp = self.kwargs.pop('type', UNDEFINED)

            elif default is not None and tp is UNDEFINED:
                tp = type(default)
        super().update(tp)
