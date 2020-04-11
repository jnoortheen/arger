# most of this module is taken from https://github.com/dusty-phillips/opterator
from enum import Enum
from inspect import isclass
from typing import Any, List, Set, Tuple

from arger.parser.docstring import parse_docstring
from arger.utils import portable_argspec


def generate_options():
    """Helper coroutine to identify short options that haven't been used yet.

    Yields lists of short option (if available) and long option for
    the given name, keeping track of which short options have been previously
    used.
    If you aren't familiar with coroutines, use similar to a generator:
    x = generate_options()
    next(x)  # advance coroutine past its initialization code
    params = x.send(param_name)
    """
    used_short_options: Set[str] = set()
    param_name = yield
    while True:
        names = ["--" + param_name]
        for letter in param_name:
            if letter not in used_short_options:
                used_short_options.add(letter)
                names.insert(0, "-" + letter)
                break
        param_name = yield names


def get_action(
    _type, default=None,
):
    if default is False:
        return "store_true"
    if default is True:
        return "store_false"
    if (_type is not UNDEFINED) and issubclass(_type, (List, Tuple)):
        return "append"
    return "store"


UNDEFINED = object()
"""sometimes the value could be None. we need this to distinguish such values."""


def get_arg_names(
    param, param_doc, option_generator,
):
    names = []

    while param_doc and param_doc[0].startswith("-"):
        names.append(param_doc.pop(0))

    return names if names else option_generator.send(param)


def add_param(
    param: str,
    param_docs: dict,
    _type: Any = UNDEFINED,
    default: Any = UNDEFINED,
    option_generator=None,
):
    """Add each function's parameter to parser

    :param param:
    :param param_docs:
    :param _type:
    :param default:
            * The default value assigned to a keyword argument helps determine
                the type of option and action.
            * The default value is assigned directly to the parser's default for that option.

            * In addition, it determines the ArgumentParser action
                * a default value of False implies store_true, while True implies store_false.
                * If the default value is a list, the action is append
                (multiple instances of that option are permitted).
                * Strings or None imply a store action.
    :param option_generator: create shorthand options from the function names

    :returns parser
    """

    param_doc = (param_docs.get(param) or "").split()
    option_kwargs = {}

    names = [param]
    if default is not UNDEFINED:
        option_kwargs["default"] = default
        option_kwargs["dest"] = param
        names = get_arg_names(param, param_doc, option_generator)

        if _type is UNDEFINED and default is not None:
            _type = type(default)

    option_kwargs.update(
        {"action": get_action(_type, default), "help": " ".join(param_doc)}
    )

    if isclass(_type) and issubclass(_type, Enum):
        option_kwargs["choices"] = [e.value for e in _type]
    elif (_type is not UNDEFINED) and _type != bool:
        option_kwargs["type"] = _type

    return (names, option_kwargs)


def prepare_arguments(
    func, param_docs,
):
    """Parses 'func' and adds parser arguments from function signature

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

            * Variable_name is the name of the variable in the function specification and
        must refer to a keyword argument. All options must have a :param: line like
        this.
    """
    (positional_params, kw_params, annotations) = portable_argspec(func)
    option_generator = generate_options()
    next(option_generator)

    arguments = []
    for param in positional_params:
        arguments.append(
            add_param(param, param_docs, _type=annotations.get(param, UNDEFINED))
        )

    for param, default in kw_params.items():
        arguments.append(
            add_param(
                param,
                param_docs,
                _type=annotations.get(param, UNDEFINED),
                default=default,
                option_generator=option_generator,
            )
        )
    return arguments


def opterate(func):
    description, param_docs = parse_docstring(func.__doc__)
    return description, prepare_arguments(func, param_docs)
