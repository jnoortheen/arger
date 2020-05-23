import inspect
from collections import OrderedDict, namedtuple
from itertools import filterfalse, tee
from typing import Dict, Iterable, Tuple

from arger.parser.docstring import parse_docstring

from ..types import UNDEFINED, T, VarArg, VarKw
from .classes import Argument, Option
from .utils import get_option_generator


Param = namedtuple("Param", ["name", "type", "help"])


def partition(pred, iterable: Iterable[T]) -> Tuple[Iterable[T], Iterable[T]]:
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filter(pred, t1), filterfalse(pred, t2)


def get_val(val, default):
    return default if val == inspect.Parameter.empty else val


def prepare_params(func, docs: Dict[str, str]):
    sign = inspect.signature(func)

    args, kwargs = partition(
        lambda x: x.default == inspect.Parameter.empty, sign.parameters.values()
    )

    def get_param(param: inspect.Parameter):
        annot = get_val(param.annotation, UNDEFINED)
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            annot = VarArg(annot)
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            annot = VarKw(annot)

        name = param.name
        return Param(name, annot, docs.get(name, ""))

    return (
        [get_param(param) for param in args],
        [(get_param(param), param.default) for param in kwargs],
    )


def create_option(param: Param, default, option_generator):
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


def create_argument(param: Param):
    arg = Argument(help=param.help)
    arg.update_flags(param.name)
    arg.update(tp=param.type)
    return arg


def prepare_arguments(func, param_docs) -> Dict[str, Option]:
    """Parse 'func' and adds parser arguments from function signature."""
    positional_params, kw_params = prepare_params(func, param_docs)
    option_generator = get_option_generator()

    arguments: Dict[str, Option] = OrderedDict()
    for param in positional_params:
        arguments[param.name] = create_argument(param)

    for param, default in kw_params:
        arguments[param.name] = create_option(param, default, option_generator)
    return arguments


def opterate(func) -> Tuple[str, Dict[str, Option]]:
    description, param_docs = parse_docstring(func.__doc__)
    return description, prepare_arguments(func, param_docs)
