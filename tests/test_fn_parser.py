from arger.parser import opterate

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
    assert args == [
        (['param1'], {'action': 'store', 'help': 'The first parameter.', 'type': int}),
        (['param2'], {'action': 'store', 'help': 'The second parameter.', 'type': str}),
        (
            ['-k', '--kw1'],
            {'action': 'store', 'default': None, 'dest': 'kw1', 'help': ''},
        ),
        (
            ['-w', '--kw2'],
            {'action': 'store_true', 'default': False, 'dest': 'kw2', 'help': '',},
        ),
    ]
