from decimal import Decimal
from enum import Enum
from typing import Annotated, List, Literal, Optional, Tuple

import pytest

from arger import Argument


class Num(Enum):
    one = "1. one"
    two = "2. two"


Num2 = Enum("Num2", "one two")

Num3 = Literal["one", "two"]


@pytest.mark.parametrize(
    "name, tp, input, expected",
    [
        # simple types
        ("an_int", int, "20", 20),
        ("a_float", float, "25", 25.0),
        ("a_deci", Decimal, "25", 25.0),
        ("a_cmplx", complex, "4+8j", 4 + 8j),
        ("a_str", str, "new-str", "new-str"),
        ("optional", Optional[str], "", None),  # noqa: UP045
        ("optional", Optional[str], "a-str", "a-str"),  # noqa: UP045
        ("optional", str | None, "a-str", "a-str"),
        ("enum", Num, "one", Num.one),
        ("enum", Num, "two", Num.two),
        ("enum", Num2, "one", Num2.one),
        ("enum", Num2, "two", Num2.two),
        ("literal", Num3, "one", "one"),
        ("literal", Num3, "two", "two"),
        # container types
        (
            "a_tuple",
            tuple,
            "1 2 3",
            ("1", "2", "3"),
        ),
        (
            "a_tuple_int",
            Tuple[int, ...],
            "1 2 3",
            (1, 2, 3),
        ),
        (
            "a_tuple_st",
            Tuple[str, ...],
            "1 2 3",
            ("1", "2", "3"),
        ),
        (
            "a_tuple_enum",
            Tuple[Num, ...],
            "one two",
            (Num.one, Num.two),
        ),
        (
            "a_tuple_literal",
            Tuple[Num3, ...],
            "one two",
            ("one", "two"),
        ),
        (
            "a_tuple_float",
            Tuple[float, ...],
            "1 2 3",
            (1.0, 2.0, 3.0),
        ),
        (
            "a_tuple_mixed",
            Tuple[str, int],
            "1 2",
            ("1", 2),
        ),
        (
            "a_tuple",
            Tuple[int, float, Decimal, complex, str],
            "1 2 30 4+4j five",
            (1, 2.0, Decimal(30), 4 + 4j, "five"),
        ),
        (
            "a_list",
            list,
            "1 2 3",
            ["1", "2", "3"],
        ),
        (
            "a_list",
            List,
            "1 2 3",
            ["1", "2", "3"],
        ),
        (
            "a_list",
            List[str],
            "1 2 3",
            ["1", "2", "3"],
        ),
        (
            "a_list",
            List[Num],
            "one two",
            [Num.one, Num.two],
        ),
        (
            "a_list",
            List[int],
            "1 2 3",
            [1, 2, 3],
        ),
        (
            "a_list",
            List[Decimal],
            "1 2 3",
            [Decimal(1), Decimal(2), Decimal(3)],
        ),
        (
            "a_set",
            set,
            "1 2 3",
            {"1", "2", "3"},
        ),
        # annotated argument
        (
            "ann_str",
            Annotated[str, Argument(metavar="var")],
            "ann",
            "ann",
        ),
        (
            "ann_enum",
            Annotated[Num, Argument(metavar="var")],
            "one",
            Num.one,
        ),
        (
            "ann_iter_enum",
            Annotated[List[Num], Argument(metavar="var")],
            "one two",
            [Num.one, Num.two],
        ),
    ],
)
def test_arguments(parser, argument, input, expected, name):
    # parses input
    ns = parser.parse_args(input.split())
    assert getattr(ns, name) == expected
