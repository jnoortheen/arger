from decimal import Decimal
from enum import Enum
from typing import List, Tuple

import pytest

from arger import Arger, Argument
from arger.funcs import Param, create_argument
from arger.typing_utils import VarArg


@pytest.fixture
def argument(name, tp, hlp='') -> Argument:
    return create_argument(Param(name, tp, hlp, []))


@pytest.fixture
def arger(argument):
    arg = Arger()
    argument.add(arg)
    return arg


class Num(Enum):
    one = '1. one'
    two = '2. two'


@pytest.mark.parametrize(
    'name, tp, input, expected',
    [
        # simple types
        ('an_int', int, '20', 20),
        ('a_float', float, '25', 25.0),
        ('a_deci', Decimal, '25', 25.0),
        ('a_cmplx', complex, '4+8j', 4 + 8j),
        ('a_str', str, 'new-str', 'new-str'),
        ('enum', Num, 'one', Num.one),
        ('enum', Num, 'two', Num.two),
        # container types
        ('vargs', VarArg, '1 2 3', ('1', '2', '3')),
        ('a_tuple', tuple, '1 2 3', ('1', '2', '3')),
        ('a_tuple', Tuple[int, ...], '1 2 3', (1, 2, 3)),
        ('a_tuple', Tuple[str, ...], '1 2 3', ('1', '2', '3')),
        ('a_tuple', Tuple[Num, ...], 'one two', (Num.one, Num.two)),
        ('a_tuple', Tuple[float, ...], '1 2 3', (1.0, 2.0, 3.0)),
        ('a_tuple', Tuple[str, int], '1 2', ('1', 2)),
        (
            'a_tuple',
            Tuple[int, float, Decimal, complex, str],
            '1 2 30 4+4j five',
            (1, 2.0, Decimal(30), 4 + 4j, 'five'),
        ),
        ('a_list', list, '1 2 3', ['1', '2', '3']),
        ('a_list', List, '1 2 3', ['1', '2', '3']),
        ('a_list', List[str], '1 2 3', ['1', '2', '3']),
        ('a_list', List[Num], 'one two', [Num.one, Num.two]),
        ('a_list', List[int], '1 2 3', [1, 2, 3]),
        ('a_list', List[Decimal], '1 2 3', [Decimal(1), Decimal(2), Decimal(3)]),
        ('a_list', set, '1 2 3', {'1', '2', '3'}),
    ],
)
def test_arguments(arger, argument, input, expected, name):
    # parses input
    ns = arger.parse_args(input.split())
    assert getattr(ns, name) == expected
