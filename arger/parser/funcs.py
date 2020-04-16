import inspect
from collections import OrderedDict, namedtuple
from typing import Any, Dict, List, Tuple

from arger.parser.docstring import parse_docstring

from ..types import UNDEFINED, VarArg, VarKw
from .classes import Argument, Option
from .utils import generate_options


Param = namedtuple('Param', ['name', 'type', 'help'])


def to_dict(p: Param):
    return p._asdict()


def prepare_params(func, docs: Dict[str, str]):
    (args, kwargs, annotations) = portable_argspec(func)

    def get_param(param):
        return Param(param, annotations.get(param, UNDEFINED), docs.get(param, ""))

    return (
        [get_param(param) for param in args],
        [(get_param(param), default) for param, default in kwargs.items()],
    )


def create_option(param: Param, default, option_generator):
    if isinstance(default, Argument):
        default.flags = [param.name]
    elif isinstance(default, Option):
        if 'dest' not in default.kwargs:
            default.kwargs['dest'] = param.name
        if not default.flags:
            default.set_flags(option_generator, param.name)
    else:
        default = Option(dest=param.name, default=default, **param._asdict())
        default.set_flags(option_generator, param.name)
    return default


def prepare_arguments(func, param_docs) -> Dict[str, Option]:
    """Parse 'func' and adds parser arguments from function signature.

    :param func: Function's signature is used to create parser
        * positional_params:
            Positional arguments become mandatory.
        * kw_params:
            All keyword arguments in the function definition are options.
            Arbitrary args and values can be captured with **kwargs
        * annotations:
            used to determine the type and action of the arguments
            list, tuple, Enum are supported, List[Enum] are supported
    :param param_docs:
        * The top part of the docstring becomes the usage message for the app.

        * Below that, ReST-style :param: lines in the following format describe the option

        * Options are further defined in the docstring.
            * the format is
            .. highlight::
                :param name: [short option and/or long option] help text
                :param variable_name: -v --verbose the help_text for the variable
                :param variable_name: -v the help_text no long option
                :param variable_name: --verbose the help_text no short option

            * variable_name is the name of the variable in the function specification and
        must refer to a keyword argument. All options must have a :param: line like
        this.
    """
    positional_params, kw_params = prepare_params(func, param_docs)
    option_generator = generate_options()
    next(option_generator)

    arguments: Dict[str, Option] = OrderedDict()
    for param in positional_params:
        arguments[param.name] = Argument(**param._asdict())

    for param, default in kw_params:
        arguments[param.name] = create_option(param, default, option_generator)
    return arguments


def opterate(func) -> Tuple[str, Dict[str, Option]]:
    description, param_docs = parse_docstring(func.__doc__)
    return description, prepare_arguments(func, param_docs)


def portable_argspec(func) -> Tuple[List[str], Dict[str, Any], Dict[str, Any]]:
    """Return function signature.

    given a function, return a tuple of
    (positional_params, keyword_params, varargs, defaults, annotations)
    where
    * positional_params is a list of parameters that don't have default values
    * keyword_params is a list of parameters that have default values
    * varargs is the string name for variable arguments
    * defaults is a dict of default values for the keyword parameters
    * annotations is a dictionary of param_name: annotation pairs
        it may be empty, and on python 2 will always be empty.
    This function is portable between Python 2 and Python 3, and does some
    extra processing of the output from inspect.
    """
    (argnames, varargs, varkw, defaults, _, _, annotations) = inspect.getfullargspec(
        func
    )

    kw_params: Dict[str, Any] = OrderedDict()
    if defaults:
        kw_boundary = len(argnames) - len(defaults)
        kw_params = {
            argnames[kw_boundary + idx]: val for idx, val in enumerate(defaults)
        }
        argnames = argnames[:kw_boundary]
    if varargs:
        argnames.append(varargs)
        annotations[varargs] = VarArg(annotations.get(varargs, str))
    if varkw:
        argnames.append(varkw)
        annotations[varkw] = VarKw(annotations.get(varkw, str))
    return (
        argnames,
        kw_params,
        annotations,
    )