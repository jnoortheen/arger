"""Integration tests configuration file."""
import re
from pathlib import Path

from nbformat import read
from pytest import param

PY_FILE = re.compile(r"[\"](.+\.py)")


def parse_example(ipy_file: Path):
    nb = read(ipy_file, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cmd = [f for f in cell.source.splitlines() if f.startswith("!")][0]
            py_file = ipy_file.with_name(cmd.split()[1])
            yield py_file, cmd, cell.outputs[0].text if cell.outputs else ""


def get_examples():
    path = Path(__file__).parent.parent.joinpath("docs", "examples")
    examples = []
    for file in path.rglob("*.ipynb"):
        examples.extend(parse_example(file))
    return examples


def get_example_params():
    for py_file, cmd, output in get_examples():  # type: (Path, str, str)
        cmds = cmd.split()
        cmds.pop(0)
        cmds.pop(0)
        cmds.insert(0, py_file.name)
        yield param(py_file, cmd, output, id="-".join(cmds).replace('.', ''))


# parameterize tests from examples directory
def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == "test_example":
        metafunc.parametrize("pyfile, cmd, expected", get_example_params())
