# pylint: disable = W0221
from argparse import Action, ArgumentParser, FileType
from typing import Any, Callable, Optional, Tuple, Union

from arger.parser.utils import FlagsGenerator

from ..typing_utils import UNDEFINED, T
from .actions import TypeAction

ARG_TYPE = Union[Callable[[str], T], FileType]


class Argument:
    flags: Tuple[str, ...] = ()

    def __init__(
        self,
        **kwargs,
    ):
        """Represent positional arguments to the command that are required by default.
        Analogous to [ArgumentParser.add_argument](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument)

        Args:
            type (ARG_TYPE): The type to which the command-line argument should be converted. Got from annotation.
            help (str): A brief description of what the argument does. From docstring.

            metavar (str): A name for the argument in usage messages.
            required (bool): Whether or not the command-line option may be omitted (optionals only).

            nargs (Union[int, str]): The number of command-line arguments that should be consumed.
                to be generated from the type-hint.
            const (Any): covered by type-hint and default value given
            choices (Iterable[str]): covered by enum type
            action (Union[str, Type[Action]]): The basic type of action to be taken
                when this argument is encountered at the command line.
        """
        if "action" not in kwargs:
            kwargs['action'] = TypeAction
        self.kwargs = kwargs

    def add(self, parser: ArgumentParser) -> Action:
        return parser.add_argument(*self.flags, **self.kwargs)

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
            *flags: The option's flags
            **kwargs: they are passed to `Argument`.
            default (Any): The value produced if the argument is absent from the command line.
                * The default value assigned to a keyword argument helps determine
                    the type of option and action if it is not type annotated.
                * The default value is assigned directly to the parser's default for that option.

                * In addition, it determines the ArgumentParser action
                    * a default value of False implies store_true, while True implies store_false.
                    * If the default value is a list, the action is append
                    (multiple instances of that option are permitted).
                    * Strings or None imply a store action.

        Examples:
            - Option('-f', '--foo', default="value")
        """
        super().__init__(**kwargs)
        self.flags = flags

    def update_flags(
        self, name: str, option_generator: Optional[FlagsGenerator] = None
    ):
        self.kwargs.setdefault('dest', name)
        if not self.flags and option_generator is not None:
            self.flags = tuple(option_generator.generate(name))

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
