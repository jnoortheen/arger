# pylint: disable=unused-variable
from arger.parser import parse_docstring

from . import samples


class describe_parse_docstring:
    def test_it_parses_google_doc(self):
        doc, params = parse_docstring(samples.google_doc.__doc__)
        assert doc == "Example function with types documented in the docstring."
        assert params == {
            "param1": "The first parameter.",
            "param2": "The second parameter.",
        }

    def test_it_parses_rest_doc(self):
        doc, params = parse_docstring(samples.rest_doc.__doc__)
        assert (
            doc
            == """Set the temperature value.
The value of the temp parameter is stored as a value in
the class variable temperature. The given value is converted
into a float value if not yet done."""
        )
        assert params == {
            "temp": "the temperature value",
            "empty": "",
            "arg2": "the temperature value multi line string to the third line",
            "arg3": "just one line",
        }
