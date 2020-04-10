"""Integration tests configuration file."""
import codecs
from pathlib import Path
from typing import Tuple

import mistune
from bs4 import BeautifulSoup


def get_text(elem) -> str:
    return elem.find(text=True, recursive=False).strip()


def get_soup(file: str):
    with codecs.open(str(file), mode="r", encoding="utf-8") as fr:
        html = mistune.html(fr.read())
        return BeautifulSoup(html, 'html.parser')


def get_scenarios(md_file: Path) -> Tuple[str, str, str]:
    soup = get_soup(str(md_file))
    titles = soup.find_all("li")
    codes = soup.find_all("code")
    for title, code in zip(titles, codes):
        cmd, out = code.text.split("\n", 1)
        yield title.text, cmd, out


def parse_example(md_file: Path):
    py_file = md_file.with_suffix(".py")
    for scenario, cmd, output in get_scenarios(md_file):
        yield py_file, scenario, cmd, output


def get_examples():
    path = Path(__file__).parent.joinpath('examples')
    examples = []
    for file in path.rglob("*.md"):
        examples.extend(parse_example(file))
    return examples


# parameterize tests from examples directory
def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == "test_example":
        idlist = []
        argvalues = []
        for py_file, _, cmd, output in get_examples():
            idlist.append(cmd)
            argvalues.append((py_file, cmd, output))
        metafunc.parametrize('pyfile, cmd, expected', argvalues, ids=idlist)
