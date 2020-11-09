# pylint: disable = protected-access
import argparse as ap
import copy
import inspect
import sys
import typing as tp
from collections import OrderedDict
from typing import Any, Tuple, Union

from arger import typing_utils as tp_utils
from arger.docstring import DocstringTp, ParamDocTp, parse_docstring

CMD_TITLE = "commands"
LEVEL = '__level__'
FUNC_PREFIX = '__func_'
NS_PREFIX = '_namespace_'
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
    kind: inspect._ParameterKind

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

    def __repr__(self):
        """helps during tests"""
        return f"<{self.__class__.__name__}: {self.flags}, {repr(self.kwargs)}>"

    def update(
        self,
        param: inspect.Parameter,
        option_generator: tp.Optional[FlagsGenerator] = None,
    ):
        self.kind = param.kind
        self._update(param, option_generator)

    def _update(
        self,
        param: inspect.Parameter,
        _: tp.Optional[FlagsGenerator] = None,
    ):
        self.flags = (param.name,)
        self._update_type(param.annotation)

    def _update_type(self, typ: tp.Any):
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

    def _update(
        self,
        param: inspect.Parameter,
        option_generator: tp.Optional[FlagsGenerator] = None,
    ):
        self.kind = param.kind
        self.kwargs.setdefault('dest', param.name)
        if not self.flags and option_generator is not None:
            self.flags = tuple(option_generator.generate(param.name))
        self.update_default(param.annotation, param.default)

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

        self._update_type(typ)


class Arger(ap.ArgumentParser):
    """Contains one (parser) or more commands (subparsers)."""

    def __init__(
        self,
        func: tp.Optional[tp.Callable] = None,
        version: tp.Optional[str] = None,
        _doc_str: tp.Optional[DocstringTp] = None,  # passed from subparser action
        _level=0,  # passed from subparser action
        **kwargs,
    ):
        """

        Args:
            func: A callable to parse root parser's arguments.
            version: adds --version flag.
            **kwargs: all the arguments that are supported by `ArgumentParser`

        Examples:
            adding version flag
                version = '%(prog)s 2.0'
                Arger() equals to Arger().add_argument('--version', action='version', version=version)
        """
        kwargs.setdefault('formatter_class', ap.ArgumentDefaultsHelpFormatter)

        self.sub_parser_action: tp.Optional[ap._SubParsersAction] = None

        self.args: tp.Dict[str, Argument] = OrderedDict()
        docstr = parse_docstring(func) if _doc_str is None else _doc_str
        kwargs.setdefault("description", docstr.description)
        kwargs.setdefault("epilog", docstr.epilog)

        super().__init__(**kwargs)

        self.set_defaults(**{LEVEL: _level})
        if func:
            self._add_arguments(func, docstr, _level)

        if version:
            self.add_argument('--version', action='version', version=version)

    def _add_arguments(self, func: tp.Callable, docstr: DocstringTp, level: int):
        option_generator = FlagsGenerator()
        sign = inspect.signature(func)

        for param in sign.parameters.values():
            param_doc = docstr.params.get(param.name)
            self.args[param.name] = create_argument(param, param_doc, option_generator)

        # parser level defaults
        self.set_defaults(**{f'{FUNC_PREFIX}{level}': self.dispatch(func)})

        for arg_name, arg in self.args.items():
            # useful only when `_namespace_` is requested or it is a kwarg
            if arg_name.startswith('_'):
                continue
            self._add_arg(arg)

    def _add_arg(self, arg: Argument):
        self.add_argument(*arg.flags, **arg.kwargs)

    def run(self, *args: str, capture_sys=True) -> ap.Namespace:
        """Parse cli and dispatch functions.

        Args:
            *args: The arguments will be passed onto self.parse_args
        """
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

        def _wrapper(fn: tp.Callable):
            return cls(func=fn, **kwargs)

        return _wrapper

    def add_cmd(self, func: tp.Callable) -> ap.ArgumentParser:
        """Decorate the function as a sub-command.

        Args:
            func: function
        """
        if not self.sub_parser_action:
            self.sub_parser_action = self.add_subparsers(title=CMD_TITLE)

        docstr = parse_docstring(func)
        return self.sub_parser_action.add_parser(
            name=func.__name__,
            help=docstr.description,
            func=func,
            _doc_str=docstr,
            _level=self.get_default(LEVEL) + 1,
        )

    def dispatch(self, fn: tp.Callable) -> tp.Any:
        """Calls the given function with args parsed from CLI"""

        def _dispatch(ns: ap.Namespace):
            kwargs = {}
            args = []
            for arg_name, arg in self.args.items():
                val = getattr(ns, arg_name)
                if arg.kind == inspect.Parameter.POSITIONAL_ONLY:
                    args.append(val)
                elif arg.kind == inspect.Parameter.VAR_POSITIONAL:
                    args.extend(val)
                else:
                    kwargs[arg_name] = val
            return fn(*args, **kwargs)

        return _dispatch


def create_argument(
    param: inspect.Parameter,
    pdoc: tp.Optional[ParamDocTp],
    option_generator: FlagsGenerator,
) -> Argument:
    hlp = pdoc.doc if pdoc else ""

    if isinstance(param.default, (Argument, Option)):
        arg = param.default
    elif param.default is _EMPTY:
        arg = Argument()
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            arg.kwargs.setdefault("nargs", "*")
            if param.annotation is not _EMPTY:
                arg.kwargs.setdefault("type", param.annotation)
    else:
        arg = Option()

    arg.kwargs.setdefault('help', hlp)
    arg.update(param, option_generator)
    return arg


def get_nargs(typ: Any) -> Tuple[Any, Union[int, str]]:
    inner = tp_utils.unpack_type(typ)
    if tp_utils.is_tuple(typ) and typ != tuple and tp_utils.get_inner_args(typ):
        args = tp_utils.get_inner_args(typ)
        inner = inner if len(set(args)) == 1 else str
        return inner, '+' if (... in args) else len(args)
    return inner, "*"


class TypeAction(ap.Action):
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
