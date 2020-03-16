import pytest
from arger import Arger

from .examples.doc_types import google_doc


@pytest.fixture
def arg():
    return Arger("Test")


def test_noargs(capsys, arg):
    """Ensure a method that expects no arguments runs properly when it receives
    none."""
    arg(google_doc)  # equivalent of calling with decorator
    with pytest.raises(SystemExit):
        arg.dispatch()  # start function

    capture = capsys.readouterr()
    assert (
        capture.err
        == """\
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: the following arguments are required: param1, param2
"""
    )
