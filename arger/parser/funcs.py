import inspect
from collections import OrderedDict
from itertools import filterfalse, tee
from typing import Dict, Iterable, List, NamedTuple, Optional, Tuple

from arger.parser.docstring import parse_docstring

from ..types import UNDEFINED, F, T, VarArg, VarKw
from .classes import Argument, Option
from .utils import FlagsGenerator


class Param(NamedTuple):
    name: str
    type: str
    help: Optional[str]
    flags: List[str]


class ParsedFunc(NamedTuple):
    description: str
    epilog: str
    args: Dict[str, Argument]


def partition(pred, iterable: Iterable[T]) -> Tuple[Iterable[T], Iterable[T]]:
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

    option = Option(help=param.help)
    option.update_flags(param.name, option_generator)
    option.update(param.type, default)
    return option


def create_argument(param: Param) -> Argument:
    arg = Argument(help=param.help)
    arg.update_flags(param.name)
    arg.update(tp=param.type)
    return arg


def parse_function(func: F) -> ParsedFunc:
    """Parse 'func' and adds parser arguments from function signature."""

    docstr, positional_params, kw_params = prepare_params(func)
    option_generator = FlagsGenerator()

    arguments: Dict[str, Argument] = OrderedDict()
    for param in positional_params:
        arguments[param.name] = create_argument(param)

    for param, default in kw_params:
        arguments[param.name] = create_option(param, default, option_generator)

    return ParsedFunc(docstr.description, docstr.epilog, arguments)
