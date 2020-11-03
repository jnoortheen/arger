import inspect
import typing as tp
from argparse import Action, ArgumentParser
from collections import OrderedDict
from itertools import filterfalse, tee

from arger.parser.docstring import parse_docstring

from ..typing_utils import UNDEFINED, T, VarArg, VarKw
from .actions import TypeAction


class Param(tp.NamedTuple):
    name: str
    type: str
    help: tp.Optional[str]
    flags: tp.List[str]


def partition(
    pred, iterable: tp.Iterable[T]
) -> tp.Tuple[tp.Iterable[T], tp.Iterable[T]]:
    """Use a predicate to partition entries into false entries and true entries"""
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filter(pred, t1), filterfalse(pred, t2)


def get_val(val, default):
    return default if val == inspect.Parameter.empty else val


def prepare_params(func):
    docstr = parse_docstring(inspect.getdoc(func))

    sign = inspect.signature(func)

    args, kwargs = partition(
        lambda x: x.default == inspect.Parameter.empty, sign.parameters.values()
    )

    def get_param(param: inspect.Parameter) -> Param:
        annot = get_val(param.annotation, UNDEFINED)
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            annot = VarArg(annot)
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            annot = VarKw(annot)

        name = param.name
        doc = docstr.params.get(name)
        return Param(name, annot, doc.doc if doc else None, doc.flags if doc else [])

    return (
        docstr,
        [get_param(param) for param in args],
        [(get_param(param), param.default) for param in kwargs],
    )


class FlagsGenerator:
    """To identify short options that haven't been used yet based on the parameter name."""

    def __init__(self):
        self.used_short_options: tp.Set[str] = set()

    def generate(self, param_name: str) -> tp.Iterator[str]:
        long_flag = "--" + param_name.replace('_', '-')
        for letter in param_name:
            if letter not in self.used_short_options:
                self.used_short_options.add(letter)
                yield "-" + letter
                break

        yield long_flag


class Argument:
    flags: tp.Tuple[str, ...] = ()

    def __init__(
        self,
        **kwargs,
    ):
        """Represent positional arguments to the command that are required by default.
        Analogous to [ArgumentParser.add_argument](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument)

        Args:
            type (Union[Callable[[str], T], FileType]): The type to which the command-line argument should be converted. Got from annotation.
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

    def update(self, tp: tp.Any = UNDEFINED, **_):
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
        self, name: str, option_generator: tp.Optional[FlagsGenerator] = None
    ):
        self.kwargs.setdefault('dest', name)
        if not self.flags and option_generator is not None:
            self.flags = tuple(option_generator.generate(name))

    def update(self, tp: tp.Any = UNDEFINED, default: tp.Any = UNDEFINED, **_):
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


class ParsedFunc(tp.NamedTuple):
    args: tp.Dict[str, Argument]
    fn: tp.Optional[tp.Callable] = None
    description: str = ''
    epilog: str = ''


def create_option(param: Param, default, option_generator: FlagsGenerator):
    if isinstance(default, Option):
        default.kwargs.setdefault('help', param.help)
        default.update_flags(param.name, option_generator)
        if 'type' not in default.kwargs:
            default.update(param.type)
        return default

    if isinstance(default, Argument):
        default.kwargs.setdefault('help', param.help)
        default.update_flags(param.name)
        if 'type' not in default.kwargs:
            default.update(param.type)
        return default

    option = Option(help=param.help or "")
    option.update_flags(param.name, option_generator)
    option.update(param.type, default)
    return option


def create_argument(param: Param) -> Argument:
    arg = Argument(help=param.help or "")
    arg.update_flags(param.name)
    arg.update(tp=param.type)
    return arg


def parse_function(func: tp.Optional[tp.Callable]) -> ParsedFunc:
    """Parse 'func' and adds parser arguments from function signature."""
    if func is None:
        return ParsedFunc({})

    docstr, positional_params, kw_params = prepare_params(func)
    option_generator = FlagsGenerator()

    arguments: tp.Dict[str, Argument] = OrderedDict()
    for param in positional_params:
        arguments[param.name] = create_argument(param)

    for param, default in kw_params:
        arguments[param.name] = create_option(param, default, option_generator)

    return ParsedFunc(arguments, func, docstr.description, docstr.epilog)
