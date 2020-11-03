# pylint: disable = W0212 ; protected member

import argparse as ap
import copy
import sys
import typing as tp

from .parser.funcs import ParsedFunc, parse_function
from .types import VarArg

CMD_TITLE = "commands"
LEVEL = '__level__'
FUNC_PREFIX = '__func_'
NS_PREFIX = '_namespace_'


class Arger(ap.ArgumentParser):
    """Contains one (parser) or more commands (subparsers)."""

    def __init__(
        self,
        func: tp.Optional[tp.Callable] = None,
        _parsed_fn: tp.Optional[ParsedFunc] = None,  # passed from subparser action
        _level=0,  # passed from subparser action
        **kwargs,
    ):
        """

        Args:
            func: A callable to parse root parser's arguments.
            **kwargs: all the arguments that are supported by `ArgumentParser`
        """
        kwargs.setdefault('formatter_class', ap.ArgumentDefaultsHelpFormatter)

        self.sub_parser_action: tp.Optional[ap._SubParsersAction] = None
        self.func = parse_function(func) if _parsed_fn is None else _parsed_fn

        if self.func.description:
            kwargs.setdefault("description", self.func.description)

        super().__init__(**kwargs)

        self._add_args(_level)

    def _add_args(self, level: int):
        self.set_defaults(**{f'{FUNC_PREFIX}{level}': self.dispatch, LEVEL: level})

        for arg_name, arg in self.func.args.items():
            if arg_name.startswith(
                '_'
            ):  # useful only when `_namespace_` is requested or it is a kwarg
                continue
            arg.add(self)

    def dispatch(self, ns: ap.Namespace) -> tp.Any:
        if self.func.fn:
            kwargs = {}
            args = []
            for arg_name, arg_type in self.func.args.items():
                val = getattr(ns, arg_name)
                if isinstance(arg_type.kwargs.get('type'), VarArg):
                    args = val
                else:
                    kwargs[arg_name] = val
            # todo: use inspect.signature.bind to bind kwargs and args to respective names
            return self.func.fn(*args, **kwargs)
        return None

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
            self.sub_parser_action = self.add_subparsers(
                # action=CommandAction,
                title=CMD_TITLE,
            )

        parsed_fn = parse_function(func)
        return self.sub_parser_action.add_parser(
            name=func.__name__,
            help=parsed_fn.description,
            _parsed_fn=parsed_fn,
            _level=self.get_default(LEVEL) + 1,
        )
