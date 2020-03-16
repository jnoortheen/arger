# pylint: disable=unused-variable
import pytest
from arger.parser import parse_docstring
from tests.examples.single_funcs import all_type_func, google_doc, rest_doc


@pytest.mark.parametrize('func', [google_doc, rest_doc])
def test_it_parses_func(func):
    doc, params = parse_docstring(func.__doc__)
    assert doc == "Example function with types documented in the docstring."
    assert params == {
        "param1": "The first parameter.",
        "param2": "The second parameter.",
    }


def test_it_creates_parser_correctly():

    doc, params = parse_docstring(all_type_func.__doc__)
    assert doc == "Example function with types documented in the docstring."
    assert params == {
        "param1": "The first parameter.",
        "param2": "The second parameter.",
    }
