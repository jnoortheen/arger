"""to show the docstring support"""

from tests.utils import Case


def _reprint(*args):
    print(*[repr(a) for a in args])


def rest_doc(param1: int, param2: str, kw1=None, kw2=False):
    """Example function with types documented in the docstring.

    :param param1: The first parameter.
    :param param2: The second parameter.
    """
    _reprint(param1, param2, kw1, kw2)


def google_doc(param1: int, param2: str, kw1=None, kw2=False):
    """Example function with types documented in the docstring.

    Args:
        param1 (int): The first parameter.
        param2: The second parameter.

    """
    _reprint(param1, param2, kw1, kw2)


GDOC_CASES = [
    Case(  # Ensure a method that expects no arguments runs properly when it receives none.
        [],
        out="",
        err="""\
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: the following arguments are required: param1, param2""",
    ),
    Case(  # assert that a help message is shown when -h is passed
        ["-h"],
        out='''\
usage: pytest [-h] [-k KW1] [-w] param1 param2

Example function with types documented in the docstring.

positional arguments:
  param1             The first parameter.
  param2             The second parameter.

optional arguments:
  -h, --help         show this help message and exit
  -k KW1, --kw1 KW1
  -w, --kw2''',
        err="",
    ),
    Case(
        ["--invalid"],
        out="",
        err="""\
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: the following arguments are required: param1, param2""",
    ),
    Case(  # pass only one positional arg
        ["p1"],
        out="",
        err="""\
usage: pytest [-h] [-k KW1] [-w] param1 param2
pytest: error: the following arguments are required: param2""",
    ),
    Case(["p1", "p2"], out="p1 p2", err='',),  # pass both required
]
