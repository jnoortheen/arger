import inspect
from decimal import Decimal

import pytest


@pytest.fixture
def parameter(name, default):
    return inspect.Parameter(
        name,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        default=default,
    )


@pytest.mark.parametrize(
    "name, default, input, expected",
    [
        # simple types
        ("an_int", 10, "20", 20),
        ("a_float", 10.0, "25", 25.0),
        ("a_deci", Decimal("10.0"), "25", Decimal("25.0")),
        ("a_cmplx", 2 + 3j, "4+8j", 4 + 8j),
        ("a_str", "a-str", "new-str", "new-str"),
        ("true", True, "--true", False),
        ("false", False, "--false", True),
        # container types
        ("a_tuple", (), "1 2 3", ("1", "2", "3")),
        ("a_list", [], "1 2 3", ["1", "2", "3"]),
    ],
)
def test_options(parser, argument, name, default, input, expected):
    # parse defaults
    ns = parser.parse_args([])
    assert getattr(ns, name) == default

    # parses input
    ns = parser.parse_args([argument.flags[0], *input.split()])
    assert getattr(ns, name) == expected
