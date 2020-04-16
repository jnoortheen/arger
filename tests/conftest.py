"""Integration tests configuration file."""
import re
from pathlib import Path
from typing import Iterator, Tuple

import mistune
from bs4 import BeautifulSoup


def get_text(elem) -> str:
    return elem.find(text=True, recursive=False).strip()


def get_soup(file: Path):
    html = mistune.html(file.read_text())
    return BeautifulSoup(html, "html.parser")


def get_scenarios(soup) -> Iterator[Tuple[str, str, str]]:
    titles = soup.find_all("h2")
    codes = soup.find_all("code", class_="language-sh")
    for title, code in zip(titles, codes):
        cmd, out = code.text.split("\n", 1)
        yield title.text, cmd, out


PY_FILE = re.compile(r"[\"](.+\.py)")


def get_pyfile(soup):
    py_file = soup.find("code", class_="language-python").text.strip()
    return PY_FILE.findall(py_file)[0]


def parse_example(md_file: Path):
    soup = get_soup(md_file)
    snippets = md_file.parent.parent.joinpath("snippets")
    py_file = snippets / get_pyfile(soup)
    for scenario, cmd, output in get_scenarios(soup):
        yield py_file, scenario, cmd, output


def get_examples():
    path = Path(__file__).parent.parent.joinpath("docs", "examples")
    examples = []
    for file in path.rglob("*.md"):
        examples.extend(parse_example(file))
    return examples


# parameterize tests from examples directory
def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == "test_example":
        idlist = []
        argvalues = []
        for py_file, _, cmd, output in get_examples():  # type: (Path, str, str, str)
            cmds = cmd.split()
            cmds.pop(0)
            cmds.pop(0)
            cmds.insert(0, py_file.name)
            idlist.append("-".join(cmds))
            argvalues.append((py_file, cmd, output))
        metafunc.parametrize("pyfile, cmd, expected", argvalues, ids=idlist)
