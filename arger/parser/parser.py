from collections import OrderedDict
from typing import Dict, Tuple

from arger.parser.docstring import parse_docstring
from arger.utils import portable_argspec

from ..types import UNDEFINED
from .classes import Argument, Option
from .utils import generate_options


def prepare_arguments(func, param_docs,) -> Dict[str, Option]:
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
    (positional_params, kw_params, annotations) = portable_argspec(func)
    option_generator = generate_options()
    next(option_generator)

    def get_args(param):
        return dict(
            flags=[param],
            help=param_docs.get(param, ""),
            type=annotations.get(param, UNDEFINED),
        )

    arguments: Dict[str, Option] = OrderedDict()
    for param in positional_params:
        arguments[param] = Argument(**get_args(param))

    for param, default in kw_params.items():
        if isinstance(default, Argument):
            default.flags = [param]
        elif isinstance(default, Option):
            if 'dest' not in default.kwargs:
                default.kwargs['dest'] = param
            if not default.flags:
                default.set_flags(option_generator)
        else:
            default = Option(dest=param, default=default, **get_args(param))
            default.set_flags(option_generator)
        arguments[param] = default
    return arguments


def opterate(func) -> Tuple[str, Dict[str, Option]]:
    description, param_docs = parse_docstring(func.__doc__)
    return description, prepare_arguments(func, param_docs)
