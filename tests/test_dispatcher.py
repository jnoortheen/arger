import re
import sys
from pathlib import Path

import pytest

from arger import Arger


@pytest.fixture
def arger(pyfile: Path) -> Arger:
    ctx: dict = {}
    exec(pyfile.read_text(), ctx)
    return ctx["arger"]


@pytest.fixture
def args(cmd: str):
    args = cmd.strip("$").strip().split(" ")
    args.pop(0)  # python
    args.pop(0)  # filename
    return args


def test_example(capsys, pyfile, arger, args, expected: str):
    if "error" in expected or expected.startswith("usage:"):
        with pytest.raises(SystemExit):
            arger.run(*args, capture_sys=False)  # start function
    else:
        arger.run(*args, capture_sys=False)

    if sys.version_info >= (3, 9):
        expected = re.sub(r"\[(?P<arg>\w+) \[(?P=arg) ...]]", r"[\g<arg> ...]", expected)
    if sys.version_info >= (3, 10):
        expected = expected.replace("optional arguments:", "options:")
    if sys.version_info >= (3, 13):
        expected = re.sub(r"(-[a-z]) (\w+|\[.+\]|\{.+\}), (--[\w-]+) \2", r"\1, \3 \2", expected)
    capture = capsys.readouterr()
    out = capture.err or capture.out
    assert out.split() == expected.split(), "".join(
        [
            f"\ncmd: {pyfile=} {args=}",
            f"\nout: \n{out}",
            f"\nexpected: \n{expected}",
        ]
    )
