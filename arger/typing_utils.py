import types
import typing
from enum import Enum
from inspect import isclass
from typing import Any, TypeVar, Union, get_args


def get_origin(tp):
    """Return the python class for the GenericAlias. Dict->dict, List->list..."""
    if getattr(tp, "__origin__", None) is not None:
        return tp.__origin__
    return tp


def match_types(tp, exp_typ) -> bool:
    """Match the given type to list of other types.

    :param tp:
    :param matches:
    """
    origin = get_origin(tp)
    if isinstance(exp_typ, str):  # instead of imported class use the class names
        if exp_typ in str(origin):
            return True
    elif get_origin(exp_typ) is origin:
        return True
    return False


def unpack_type(tp, default=str) -> Any:
    """Unpack subscripted type for use with argparser.

    Args:
        tp:
        default:

    Returns:
        type inside the container type
    """
    args = get_args(tp)
    if args and str(args[0]) not in {"~T", "typing.Any"}:
        return args[0]
    return default


def is_seq_container(tp):
    origin = get_origin(tp)
    return origin in {list, tuple, set, frozenset}


def is_enum(tp):
    return isclass(tp) and issubclass(tp, Enum)


def is_literal(tp):
    """since Literal could be imported from either typing/typing_extensions we use the name of cls to check"""
    return match_types(tp, ".Literal")


def has_annotated(typ) -> bool:
    return typing.get_origin(typ) is typing.Annotated


def get_literal_params(typ):
    params = tuple(get_args(typ))
    factory_type = type(params[0]) if params else str
    return params, factory_type


def is_tuple(tp) -> bool:
    return match_types(tp, tuple)


def is_optional(tp) -> bool:
    """Check that tp = typing.Optional[typ1]"""
    if match_types(tp, Union) or isinstance(tp, types.UnionType):
        args = get_args(tp)
        if len(args) == 2:
            return type(None) in args
    return False


def cast(tp, val) -> Any:
    # https://github.com/contains-io/typingplus/blob/master/typingplus.py
    # for advanced casting one should use pydantic
    origin = get_origin(tp)
    if is_enum(origin):
        if isinstance(val, origin):
            return val
        return origin[val]

    if is_literal(origin):
        _, typ = get_literal_params(origin)
        return typ(val)

    if is_seq_container(origin):
        val = origin(val)
        args = get_args(tp)
        if (
            origin
            in {
                tuple,
            }
            and args
            and Ellipsis not in args
        ):
            return tuple(cast(args[idx], v) for idx, v in enumerate(val))
        return origin([cast(unpack_type(tp), v) for v in val])

    return origin(val)


T = TypeVar("T")


def get_annotated_args(typ):
    origin, *params = typing.get_args(typ)
    return origin, (params[0] if params else None)
