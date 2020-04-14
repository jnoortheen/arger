from collections import OrderedDict

from arger.parser import opterate
from arger.parser.classes import Argument

from .utils import _reprint


def main(param1: int, param2: str, kw1=None, kw2=False):
    """Example function with types documented in the docstring.

    :param param1: The first parameter.
    :param param2: The second parameter.
    """
    _reprint(**locals())


def test_opterate():
    doc, args = opterate(func=main)
    assert doc == "Example function with types documented in the docstring."
    assert list(args) == ['param1', 'param2', 'kw1', 'kw2']

    assert [v.flags for v in args.values()] == [
        ['param1'],
        ['param2'],
        ['-k', '--kw1'],
        ['-w', '--kw2'],
    ]

    assert [v.kwargs for v in args.values()] == [
        {'action': 'store', 'help': 'The first parameter.', 'type': int,},
        {'action': 'store', 'help': 'The second parameter.', 'type': str,},
        {'action': 'store', 'default': None, 'dest': 'kw1', 'help': '',},
        {'action': 'store_true', 'default': False, 'dest': 'kw2', 'help': '',},
    ]
