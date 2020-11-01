from pathlib import Path
import re
import pytest
from colorama import Back, Fore, Style

from arger import Arger
import sys


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

    if sys.version_info >= (3, 9):
        expected = re.sub(
            r'\[(?P<arg>\w+) \[(?P=arg) ...]]', r'[\g<arg> ...]', expected
        )
    capture = capsys.readouterr()
    out = capture.err or capture.out
    assert out.split() == expected.split(), ''.join(
        [
            f"\n{Fore.BLUE}{Back.WHITE}cmd: {Style.RESET_ALL}\n{args}",
            f"\n{Fore.BLUE}{Back.WHITE}out: {Style.RESET_ALL}\n{out}",
            f"\n{Fore.BLUE}{Back.WHITE}expected: {Style.RESET_ALL}\n{expected}",
        ]
    )
