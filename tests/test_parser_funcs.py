import pytest

from arger.parser import opterate
from arger.parser.actions import TypeAction
from arger.parser.funcs import Param, create_option
from arger.parser.utils import get_option_generator
from arger.types import UNDEFINED, VarArg

from .utils import _reprint


def main(param1: int, param2: str, kw1=None, kw2=False, *args: int):
    """Example function with types documented in the docstring.

    :param param1: The first parameter.
    :param param2: The second parameter.
    """
    _reprint(**locals())


def test_opterate():
    doc, args = opterate(func=main)
    assert doc == "Example function with types documented in the docstring."
    exp_args = ["param1", "param2", "args", "kw1", "kw2"]
    assert list(args) == exp_args

    exp_flags = [
        ["param1"],
        ["param2"],
        ["args"],
        ["-k", "--kw1"],
        ["-w", "--kw2"],
    ]
    exp_kwargs = [
        {"action": TypeAction, "help": "The first parameter.", "type": int,},
        {"action": TypeAction, "help": "The second parameter.", "type": str,},
        {"action": TypeAction, "help": "", "type": VarArg(int)},
        {"action": TypeAction, "default": None, "dest": "kw1", "help": "",},
        {"action": "store_true", "default": False, "dest": "kw2", "help": "",},
    ]

    for idx, arg in enumerate(args.values()):
        assert arg.flags == exp_flags[idx]
        assert arg.kwargs == exp_kwargs[idx]


@pytest.fixture
def gen_options():
    return get_option_generator()


@pytest.fixture
def param(name, tp=UNDEFINED, hlp=''):
    return Param(name, tp, hlp)


@pytest.mark.parametrize(
    'name, default, expected', [('an_int', 10, ''),],
)
def test_create_option(
    gen_options, param, default, expected,
):
    option = create_option(param, default, gen_options)
    assert str(option) == expected
