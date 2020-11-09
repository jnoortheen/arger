# pylint: disable = protected-access

import argparse as ap
import copy
import inspect
import sys
import typing as tp
from collections import OrderedDict

from arger.docstring import DocstringTp, parse_docstring
from arger.funcs import Argument, FlagsGenerator, create_argument

CMD_TITLE = "commands"
LEVEL = '__level__'
FUNC_PREFIX = '__func_'
NS_PREFIX = '_namespace_'


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
