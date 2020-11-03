import argparse
import inspect
import typing as tp
from argparse import Action, ArgumentParser
from collections import OrderedDict
from itertools import filterfalse, tee
from typing import Any, Tuple, Union

from arger import typing_utils as tp_utils
from arger.docstring import parse_docstring


class Param(tp.NamedTuple):
    name: str
    type: str
    help: tp.Optional[str]
    flags: tp.List[str]


def partition(
    pred, iterable: tp.Iterable[tp_utils.T]
) -> tp.Tuple[tp.Iterable[tp_utils.T], tp.Iterable[tp_utils.T]]:
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
        annot = get_val(param.annotation, tp_utils.UNDEFINED)
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            annot = tp_utils.VarArg(annot)
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            annot = tp_utils.VarKw(annot)

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
        Analogous to
        [ArgumentParser.add_argument](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument)

        Args:
            type (Union[Callable[[str], T], FileType]): The type to which the command-line argument should be converted.
                Got from annotation.
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

    def set_dest(self, name: str, typ: tp.Any):
        self.flags = (name,)
        self.update_type(typ)

    def update_type(self, typ: tp.Any):
        """Update type externally."""
        if 'type' not in self.kwargs and typ is not tp_utils.UNDEFINED:
            self.kwargs['type'] = typ


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

    def set_flags(
        self,
        name: str,
        typ: tp.Any,
        default: tp.Any = tp_utils.UNDEFINED,
        option_generator: tp.Optional[FlagsGenerator] = None,
    ):
        self.kwargs.setdefault('dest', name)
        if not self.flags and option_generator is not None:
            self.flags = tuple(option_generator.generate(name))
        self.update_default(typ, default)

    def update_default(self, typ: tp.Any, default: tp.Any = tp_utils.UNDEFINED):
        """Update type and default externally"""
        if default is not tp_utils.UNDEFINED and 'default' not in self.kwargs:
            self.kwargs["default"] = default
        else:
            default = self.kwargs["default"]

        if isinstance(default, bool):
            self.kwargs['action'] = "store_true" if default is False else "store_false"
            typ = self.kwargs.pop('type', tp_utils.UNDEFINED)
        elif default is not None and typ is tp_utils.UNDEFINED:
            typ = type(default)

        self.update_type(typ)


class ParsedFunc(tp.NamedTuple):
    args: tp.Dict[str, Argument]
    fn: tp.Optional[tp.Callable] = None
    description: str = ''
    epilog: str = ''


def create_option(param: Param, default, option_generator: FlagsGenerator):
    if isinstance(default, Option):
        default.kwargs.setdefault('help', param.help)
        default.set_flags(param.name, param.type, option_generator)
        return default

    if isinstance(default, Argument):
        default.kwargs.setdefault('help', param.help)
        default.set_dest(param.name, param.type)
        return default

    option = Option(help=param.help or "")
    option.set_flags(param.name, param.type, default, option_generator)
    return option


def create_argument(param: Param) -> Argument:
    arg = Argument(help=param.help or "")
    arg.set_dest(param.name, param.type)
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


def get_nargs(typ: Any) -> Tuple[Any, Union[int, str]]:
    inner = tp_utils.unpack_type(typ)
    if (
        tp_utils.is_tuple(typ)
        and typ != tuple
        and not isinstance(typ, (tp_utils.VarKw, tp_utils.VarArg))
        and tp_utils.get_inner_args(typ)
    ):
        args = tp_utils.get_inner_args(typ)
        inner = inner if len(set(args)) == 1 else str
        return inner, '+' if (... in args) else len(args)
    return inner, "*"


class TypeAction(argparse.Action):
    """After the parse update the type of value"""

    def __init__(self, *args, **kwargs):
        typ = kwargs.pop("type", tp_utils.UNDEFINED)
        self.orig_type = typ
        if typ is not tp_utils.UNDEFINED:
            origin = tp_utils.get_origin(typ)
            if tp_utils.is_iterable(origin):
                origin, kwargs["nargs"] = get_nargs(typ)

            if tp_utils.is_enum(origin):
                kwargs.setdefault("choices", [e.name for e in origin])
                origin = str

            kwargs["type"] = origin
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if tp_utils.is_iterable(self.orig_type):
            items = getattr(namespace, self.dest, ()) or ()
            items = list(items)
            items.extend(values)
            vals = items
        else:
            vals = values
        setattr(namespace, self.dest, tp_utils.cast(self.orig_type, vals))
