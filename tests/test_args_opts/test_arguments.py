from decimal import Decimal
from enum import Enum
from typing import List, Tuple

import pytest


class Num(Enum):
    one = '1. one'
    two = '2. two'


Num2 = Enum("Num2", "one two")


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
        ('enum', Num2, 'one', Num2.one),
        ('enum', Num2, 'one', Num2.one),
        # container types
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
def test_arguments(parser, argument, input, expected, name):
    # parses input
    ns = parser.parse_args(input.split())
    assert getattr(ns, name) == expected
