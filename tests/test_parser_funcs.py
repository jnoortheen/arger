from arger.main import Arger, TypeAction

from .utils import _reprint


def main(param1: int, param2: str, kw1=None, kw2=False, *args: int):
    """Example function with types documented in the docstring.

    :param param1: The first parameter.
    :param param2: The second parameter.
    """
    _reprint(**locals())


def test_parse_function():
    docs = Arger(func=main)
    assert docs.description == "Example function with types documented in the docstring."
    exp_args = ["param1", "param2", "kw1", "kw2", "args"]
    assert list(docs.args) == exp_args

    exp_flags = [
        ("param1",),
        ("param2",),
        ("-k", "--kw1"),
        ("-w", "--kw2"),
        ("args",),
    ]
    exp_kwargs = [
        {
            "action": TypeAction,
            "help": "The first parameter.",
            "type": int,
        },
        {
            "action": TypeAction,
            "help": "The second parameter.",
            "type": str,
        },
        {
            "default": None,
            "dest": "kw1",
            "help": "",
        },
        {
            "action": "store_true",
            "default": False,
            "dest": "kw2",
            "help": "",
        },
        {"action": TypeAction, "help": "", "type": int, "nargs": "*"},
    ]

    for idx, arg in enumerate(docs.args.values()):
        assert arg.flags == exp_flags[idx]
        assert arg.kwargs == exp_kwargs[idx]
