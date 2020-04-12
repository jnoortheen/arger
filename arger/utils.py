import inspect
from typing import Any, List, Tuple


def portable_argspec(func):
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
    (argnames, _, _, defaults, _, _, annotations,) = inspect.getfullargspec(func)

    kw_params = {}
    if defaults:
        kw_boundary = len(argnames) - len(defaults)
        kw_params = {
            argnames[kw_boundary + idx]: val for idx, val in enumerate(defaults)
        }
        argnames = argnames[:kw_boundary]

    return (
        argnames,
        kw_params,
        annotations,
    )


def match_types(type, *matches):
    """Match the given type to list of other types.

    :param type:
    :param matches:

    >>> match_types(List, List[str], List, Tuple, Tuple[str], Tuple[Any])
    True
    >>> match_types(List[str], List[Any])
    True
    >>> match_types(List[str], List)
    True
    """
    return any([str(m).startswith(str(type)) for m in matches])
