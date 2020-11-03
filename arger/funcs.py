import argparse
import inspect
import typing as tp
from argparse import Action, ArgumentParser
from collections import OrderedDict
from typing import Any, Tuple, Union

from arger import typing_utils as tp_utils
from arger.docstring import ParamDocTp, parse_docstring

_EMPTY = inspect.Parameter.empty


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
        if 'type' not in self.kwargs and typ is not _EMPTY:
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
        default: tp.Any = _EMPTY,
        option_generator: tp.Optional[FlagsGenerator] = None,
    ):
        self.kwargs.setdefault('dest', name)
        if not self.flags and option_generator is not None:
            self.flags = tuple(option_generator.generate(name))
        self.update_default(typ, default)

    def update_default(self, typ: tp.Any, default: tp.Any = _EMPTY):
        """Update type and default externally"""
        if default is not _EMPTY and 'default' not in self.kwargs:
            self.kwargs["default"] = default
        else:
            default = self.kwargs["default"]

        if isinstance(default, bool):
            self.kwargs['action'] = "store_true" if default is False else "store_false"
            typ = self.kwargs.pop('type', _EMPTY)
        elif default is not None and typ is _EMPTY:
            typ = type(default)

        self.update_type(typ)


class ParsedFunc:
    fn: tp.Optional[tp.Callable] = None
    description: str = ''
    epilog: str = ''
    args: tp.Dict[str, Argument]

    def __init__(self, func: tp.Optional[tp.Callable]):
        """Parse 'func' and adds parser arguments from function signature."""
        if func is None:
            self.args = {}
            return

        docstr = parse_docstring(inspect.getdoc(func))

        sign = inspect.signature(func)
        self.fn = func
        self.description = docstr.description
        self.epilog = docstr.epilog

        option_generator = FlagsGenerator()
        self.args = OrderedDict()
        for param in sign.parameters.values():
            param_doc = docstr.params.get(param.name)
            if param.default is param.empty:
                self.args[param.name] = create_argument(param, param_doc)
            else:
                self.args[param.name] = create_option(
                    param, param_doc, option_generator
                )

    def dispatch(self, ns: argparse.Namespace) -> tp.Any:
        if self.fn:
            kwargs = {}
            args = []
            sign = inspect.signature(self.fn)
            for arg_name in self.args:
                val = getattr(ns, arg_name)
                param = sign.parameters[arg_name]
                if param.kind == param.POSITIONAL_ONLY:
                    args.append(val)
                elif param.kind == param.VAR_POSITIONAL:
                    args.extend(val)
                else:
                    kwargs[arg_name] = val
            return self.fn(*args, **kwargs)
        return None


def create_option(
    param: inspect.Parameter,
    pdoc: tp.Optional[ParamDocTp],
    option_generator: FlagsGenerator,
):
    hlp = pdoc.doc if pdoc else ""
    if isinstance(param.default, Option):
        param.default.kwargs.setdefault('help', hlp)
        param.default.set_flags(param.name, param.annotation, option_generator)
        return param.default

    if isinstance(param.default, Argument):
        param.default.kwargs.setdefault('help', hlp)
        param.default.set_dest(param.name, param.annotation)
        return param.default

    option = Option(help=hlp)
    option.set_flags(param.name, param.annotation, param.default, option_generator)
    return option


def create_argument(param: inspect.Parameter, doc: tp.Optional[ParamDocTp]) -> Argument:
    kwargs = dict(help=doc.doc if doc else "")
    if param.kind == inspect.Parameter.VAR_POSITIONAL:
        kwargs.setdefault("nargs", "*")
        if param.annotation is not _EMPTY:
            kwargs.setdefault("type", param.annotation)
    arg = Argument(**kwargs)
    arg.set_dest(param.name, param.annotation)
    return arg


def get_nargs(typ: Any) -> Tuple[Any, Union[int, str]]:
    inner = tp_utils.unpack_type(typ)
    if tp_utils.is_tuple(typ) and typ != tuple and tp_utils.get_inner_args(typ):
        args = tp_utils.get_inner_args(typ)
        inner = inner if len(set(args)) == 1 else str
        return inner, '+' if (... in args) else len(args)
    return inner, "*"


class TypeAction(argparse.Action):
    """After the parse update the type of value"""

    def __init__(self, *args, **kwargs):
        typ = kwargs.pop("type", _EMPTY)
        self.orig_type = typ
        self.is_iterable = tp_utils.is_seq_container(typ)
        self.is_enum = False
        if typ is not _EMPTY:
            origin = tp_utils.get_origin(typ)
            if self.is_iterable:
                origin, kwargs["nargs"] = get_nargs(typ)

            if tp_utils.is_enum(origin):
                kwargs.setdefault("choices", [e.name for e in origin])
                origin = str
                self.is_enum = True

            kwargs["type"] = origin
        super().__init__(*args, **kwargs)

    def cast_value(self, vals):
        if self.is_iterable or self.is_enum:
            return tp_utils.cast(self.orig_type, vals)
        return vals

    def __call__(self, parser, namespace, values, option_string=None):
        if self.is_iterable:
            items = getattr(namespace, self.dest, ()) or ()
            items = list(items)
            items.extend(values)
            vals = items
        else:
            vals = values
        setattr(namespace, self.dest, self.cast_value(vals))
