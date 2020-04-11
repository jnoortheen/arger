import argparse
from typing import Callable


class Option:
    def __init__(
        self,
        type: Callable,
        default=None,
        flags: str = None,
        help: str = None,
        metavar: str = None,
        required=False,
    ):
        """represents optional arguments to the command.
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
    """represents positional argument and are required."""

    def __init__(self, type: Callable, help: str = None, metavar: str = None):
        super().__init__(type, help=help, metavar=metavar, required=True)
