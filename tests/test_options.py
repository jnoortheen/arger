import pytest
from decimal import Decimal

from arger import Arger
from arger.parser.classes import Option
from arger.parser.funcs import Param, create_option
from arger.parser.utils import get_option_generator
from arger.types import UNDEFINED


@pytest.fixture
def gen_options():
    return get_option_generator()


@pytest.fixture
def option(default, name, gen_options, tp=UNDEFINED, hlp='') -> Option:
    return create_option(Param(name, tp, hlp), default, gen_options)


@pytest.fixture
def arger(option):
    arg = Arger()
    option.add(arg)
    return arg


@pytest.mark.parametrize(
    'name, default, input, expected',
    [
        # simple types
        ('an_int', 10, '20', 20),
        ('a_float', 10.0, '25', 25.0),
        ('a_deci', Decimal('10.0'), '25', Decimal('25.0')),
        ('a_cmplx', 2 + 3j, '4+8j', 4 + 8j),
        ('a_str', 'a-str', 'new-str', 'new-str'),
        ('true', True, '--true', False),
        ('false', False, '--false', True),
        # container types
        ('a_tuple', (), '1 2 3', ('1', '2', '3')),
        ('a_list', [], '1 2 3', ['1', '2', '3']),
    ],
)
def test_options(arger, option, name, default, input, expected):
    # parse defaults
    ns = arger.parse_args([])
    assert getattr(ns, name) == default

    # parses input
    ns = arger.parse_args([option.flags[0]] + input.split())
    assert getattr(ns, name) == expected
