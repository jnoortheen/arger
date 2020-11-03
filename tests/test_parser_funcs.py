from arger.funcs import ParsedFunc, TypeAction
from arger.typing_utils import VarArg

from .utils import _reprint


def main(param1: int, param2: str, kw1=None, kw2=False, *args: int):
    """Example function with types documented in the docstring.

    :param param1: The first parameter.
    :param param2: The second parameter.
    """
    _reprint(**locals())


def test_parse_function():
    docs = ParsedFunc(func=main)
    assert (
        docs.description == "Example function with types documented in the docstring."
    )
    exp_args = ["param1", "param2", "args", "kw1", "kw2"]
    assert list(docs.args) == exp_args

    exp_flags = [
        ("param1",),
        ("param2",),
        ("args",),
        ("-k", "--kw1"),
        ("-w", "--kw2"),
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
        {"action": TypeAction, "help": "", "type": VarArg(int)},
        {
            "action": TypeAction,
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
    ]

    for idx, arg in enumerate(docs.args.values()):
        assert arg.flags == exp_flags[idx]
        assert arg.kwargs == exp_kwargs[idx]
