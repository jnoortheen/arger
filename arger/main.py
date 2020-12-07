# pylint: disable = protected-access,unused-argument,redefined-builtin
import argparse as ap
import copy
import inspect
import sys
import typing as tp
from collections import OrderedDict

from arger import typing_utils as tp_utils
from arger.docstring import DocstringParser, DocstringTp, ParamDocTp

LEVEL = "__level__"
FUNC_PREFIX = "__func_"
NS_PREFIX = "_namespace_"
_EMPTY = inspect.Parameter.empty


class FlagsGenerator:
    """To identify short options that haven't been used yet based on the parameter name."""

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.used_short_options: tp.Set[str] = set()

    def generate(self, param_name: str) -> tp.Iterator[str]:
        long_flag = (self.prefix * 2) + param_name.replace("_", "-")
        for letter in param_name:
            if letter not in self.used_short_options:
                self.used_short_options.add(letter)
                yield self.prefix + letter
                break

        yield long_flag


class Argument:
    kind: inspect._ParameterKind

    def __init__(
        self,
        *,
        type: tp.Union[tp.Callable[[str], tp_utils.T], ap.FileType] = None,
        metavar: str = None,
        required: bool = None,
        nargs: tp.Union[int, str] = None,
        const: tp.Any = None,
        choices: tp.Iterable[str] = None,
        action: tp.Union[str, tp.Type[ap.Action]] = None,
        flags: tp.Sequence[str] = (),
        **kwargs: tp.Any,
    ):
        """Represent positional arguments to the command that are required by default.
        Analogous to
        [ArgumentParser.add_argument](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument)

        Args:
            type: The type to which the command-line argument should be converted.

                Got from annotation.
                Use Argument class itself in case you want to pass variables to `Arger.add_argument`.

                Ex: `typing.cast(int, Argument(type=int))`. If not passed then it is returned as str.

            metavar: A name for the argument in usage messages.

            nargs: The number of command-line arguments that should be consumed.
                to be generated from the type-hint.

                Ex: types and how they are converted to nargs

                * `Tuple[str, ...] -> nargs='+'`
                * `Tuple[str, str] -> nargs=2`
                * `List[str]|tuple|list -> nargs=*`

                Note: even though Tuple[str,...] doesn't mean one or more, it is just to make `nargs=+` easier to add.

            const: covered by type-hint and default value given
            choices: Use `enum.Enum` as the typehint to generate choices automatically.
            action: The basic type of action to be taken
                when this argument is encountered at the command line.

            flags: It will be generated from the argument name.
                In case one wants to override the generated flags, could be done by passing them.

            default (tp.Any): The value produced if the argument is absent from the command line.

                * The default value assigned to a keyword argument helps determine
                    the type of option and action if it is not type annotated.
                * The default value is assigned directly to the parser's default for that option.
                * In addition, it determines the ArgumentParser action
                    * a default value of False implies store_true, while True implies store_false.
                    * If the default value is a list, the action is append
                    (multiple instances of that option are permitted).
                    * Strings or None imply a store action.

            kwargs: it is delegated to `ArgumentParser.add_argument` method.
        """
        for var_name in (
            "type",
            "metavar",
            "required",
            "nargs",
            "const",
            "choices",
            "action",
        ):
            value = locals()[var_name]
            if value is not None:
                kwargs[var_name] = value
        if "action" not in kwargs:
            kwargs["action"] = TypeAction
        self.flags = flags
        self.kwargs = kwargs

    def __repr__(self):
        """helps during tests"""
        return f"<{self.__class__.__name__}: {self.flags}, {repr(self.kwargs)}>"

    @classmethod
    def create(
        cls,
        param: inspect.Parameter,
        pdoc: tp.Optional[ParamDocTp],
        option_generator: FlagsGenerator,
    ) -> "Argument":
        hlp = pdoc.doc if pdoc else ""

        if isinstance(param.annotation, Argument):
            arg = param.annotation
        else:
            arg = Argument()

        arg.kwargs.setdefault("help", hlp)
        arg.update(param, option_generator)
        return arg

    def update(
        self,
        param: inspect.Parameter,
        option_generator: FlagsGenerator,
    ):
        self.kind = param.kind
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            self.kwargs.setdefault("nargs", "*")
        self._update(param, option_generator)
        self._update_type(param.annotation)

    def _update(
        self,
        param: inspect.Parameter,
        option_generator: FlagsGenerator,
    ):
        if param.default is _EMPTY:  # it will become a positional argument
            self.flags = (param.name,)
        else:  # it will become a flat
            self.kwargs.setdefault("dest", param.name)
            if not self.flags:
                self.flags = tuple(option_generator.generate(param.name))
            self._update_default(param.annotation, param.default)

    def _update_type(self, typ: tp.Any):
        """Update type from annotation."""
        if (
            (typ is not _EMPTY)
            and (not isinstance(typ, Argument))
            and ("type" not in self.kwargs)
        ):
            self.kwargs.setdefault("type", typ)

    def _update_default(self, typ: tp.Any, default: tp.Any):
        """Update type and default externally"""
        if "default" not in self.kwargs:
            self.kwargs["default"] = default
        else:
            default = self.kwargs["default"]

        if isinstance(default, bool):
            self.kwargs["action"] = "store_true" if default is False else "store_false"
            typ = self.kwargs.pop("type", _EMPTY)
        elif default is not None and typ is _EMPTY:
            typ = type(default)

        self._update_type(typ)

    def add_to(self, parser: "Arger"):
        return parser.add_argument(*self.flags, **self.kwargs)


class Arger(ap.ArgumentParser):
    """Contains one (parser) or more commands (subparsers)."""

    def __init__(
        self,
        func: tp.Optional[tp.Callable] = None,
        version: tp.Optional[str] = None,
        sub_parser_title="commands",
        formatter_class=ap.ArgumentDefaultsHelpFormatter,
        exceptions_to_catch: tp.Sequence[tp.Type[Exception]] = (),
        _doc_str: tp.Optional[DocstringTp] = None,
        _level=0,
        **kwargs,
    ):
        """

        Args:
            func: A callable to parse root parser's arguments.
            version: adds --version flag.
            sub_parser_title: sub-parser title to pass.
            exceptions_to_catch: exceptions to catch and print its message.
                Will exit with 1 and will hide traceback.

            _doc_str: internally passed from arger.add_cmd
            _level: internal

            **kwargs: all the arguments that are supported by
                    [ArgumentParser](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser)

        Examples:
            adding version flag
                version = '%(prog)s 2.0'
                Arger() equals to Arger().add_argument('--version', action='version', version=version)
        """
        kwargs.setdefault("formatter_class", formatter_class)

        self.sub_parser_title = sub_parser_title
        self.sub_parser: tp.Optional[ap._SubParsersAction] = None

        self.args: tp.Dict[str, Argument] = OrderedDict()
        docstr = DocstringParser.parse(func) if _doc_str is None else _doc_str
        kwargs.setdefault("description", docstr.description)
        kwargs.setdefault("epilog", docstr.epilog)

        super().__init__(**kwargs)

        self.set_defaults(**{LEVEL: _level})
        self.func = func
        self.exceptions_to_catch = exceptions_to_catch
        self._add_arguments(docstr, _level)

        if version:
            self.add_argument("--version", action="version", version=version)

    def _add_arguments(self, docstr: DocstringTp, level: int):
        if not self.func:
            return
        option_generator = FlagsGenerator(self.prefix_chars)
        sign = inspect.signature(self.func)

        for param in sign.parameters.values():
            param_doc = docstr.params.get(param.name)
            self.args[param.name] = Argument.create(param, param_doc, option_generator)

        # parser level defaults
        self.set_defaults(**{f"{FUNC_PREFIX}{level}": self._dispatch})

        for arg_name, arg in self.args.items():
            # useful only when `_namespace_` is requested or it is a kwarg
            if arg_name.startswith("_"):
                continue
            arg.add_to(self)

    def run(self, *args: str, capture_sys=True, **kwargs) -> ap.Namespace:
        """Parse cli and dispatch functions.

        Args:
            capture_sys: whether to capture `sys.argv` if `args` not passed. Useful during testing.
            *args: The arguments will be passed onto as `self.parse_args(args)`.
            **kwargs: will get passed to `parse_args` method
        """
        if not args and capture_sys:
            args = tuple(sys.argv[1:])
        namespace = self.parse_args(args, **kwargs)
        kwargs = vars(namespace)
        kwargs[NS_PREFIX] = copy.copy(namespace)
        kwargs["_arger_"] = self
        # dispatch all functions as in hierarchy
        for level in range(kwargs.get(LEVEL, 0) + 1):
            func_name = f"{FUNC_PREFIX}{level}"
            if func_name in kwargs:
                kwargs[func_name](**kwargs)

        return namespace

    @classmethod
    def init(cls, **kwargs) -> tp.Callable[[tp.Callable], "Arger"]:
        """Create parser from function as a decorator.

        Args:
            **kwargs: will be passed to arger.Arger initialisation.
        """

        def _wrapper(fn: tp.Callable):
            return cls(func=fn, **kwargs)

        return _wrapper

    @tp.overload
    def add_cmd(self, func: tp.Callable) -> "Arger":
        ...

    @tp.overload
    def add_cmd(self, func: None, **kwargs) -> tp.Callable[[tp.Callable], "Arger"]:
        ...

    def add_cmd(self, func=None, **kwargs):
        """Create a sub-command from the function.
        All its parameters will be converted to CLI args wrt their types.

        Args:
            func: function to create sub-command from.
            **kwargs: will get passed to `subparser.add_parser` method

        Returns
            Arger: A new parser from the function is returned.
        """
        if not self.sub_parser:
            self.sub_parser = self.add_subparsers(title=self.sub_parser_title)

        def _wrapper(fn: tp.Callable) -> "Arger":
            docstr = DocstringParser.parse(fn)
            arger = self.sub_parser.add_parser(  # type: ignore
                name=kwargs.pop("name", fn.__name__),
                help=kwargs.pop("help", docstr.description),
                func=fn,
                _doc_str=docstr,
                _level=self.get_default(LEVEL) + 1,
                **kwargs,
            )
            return tp.cast(Arger, arger)

        if func is None:
            return _wrapper
        return _wrapper(func)

    def add_commands(self, *func: tp.Callable) -> tp.Tuple["Arger", ...]:
        """Add multiple sub-commands to the main command at once"""
        return tuple(self.add_cmd(fn) for fn in func)

    def _dispatch(self, **ns: tp.Any) -> tp.Any:
        """Calls the given function with args parsed from CLI

        Args:
            ns: namespace after parsing
        """

        kwargs = {}
        args = []
        for arg_name, arg in self.args.items():
            val = ns[arg_name]
            if arg.kind in {
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            }:
                args.append(val)
            elif arg.kind == inspect.Parameter.VAR_POSITIONAL:
                args.extend(val)
            else:
                kwargs[arg_name] = val
        return self.func(*args, **kwargs) if self.func else None


def get_nargs(typ: tp.Any) -> tp.Tuple[tp.Any, tp.Union[int, str]]:
    inner = tp_utils.unpack_type(typ)
    if tp_utils.is_tuple(typ) and typ != tuple and tp_utils.get_inner_args(typ):
        args = tp_utils.get_inner_args(typ)
        inner = inner if len(set(args)) == 1 else str
        return inner, "+" if (... in args) else len(args)
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
