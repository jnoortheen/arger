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


def test_example(capsys, arger, args, expected: str):
    if "error" in expected or expected.startswith("usage:"):
        with pytest.raises(SystemExit):
            arger.run(*args, capture_sys=False)  # start function
    else:
        arger.run(*args, capture_sys=False)

    capture = capsys.readouterr()
    out = capture.err or capture.out
    assert (
        out.split() == expected.split()
    ), f"\ncmd: {args}\nout: \n{out}\nexpected:\n{expected}\n"
