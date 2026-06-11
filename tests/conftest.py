"""Integration tests configuration file."""

from collections.abc import Iterator
from pathlib import Path

from pytest import param


def parse_markdown_example(md_file: Path):
    content = md_file.read_text()
    lines = content.splitlines()
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if line == "```console":
            idx += 1
            if idx < len(lines):
                cmd_line = lines[idx].strip()
                command = cmd_line[2:].strip() if cmd_line.startswith("$ ") else cmd_line.strip()

                expected_lines = []
                idx += 1
                while idx < len(lines) and lines[idx].strip() != "```":
                    expected_lines.append(lines[idx])
                    idx += 1
                expected = "\n".join(expected_lines)
                if expected:
                    expected += "\n"

                py_file_name = None
                for token in command.split():
                    if token.endswith(".py"):
                        py_file_name = token
                        break
                if py_file_name:
                    py_file_path = md_file.parent.parent.parent / py_file_name
                    yield py_file_path, f"!{command}", expected
        idx += 1


def get_examples() -> Iterator[tuple[Path, str, str]]:
    path = Path(__file__).parent.parent.joinpath("docs", "examples")
    for file in path.glob("*.md"):
        yield from parse_markdown_example(file)


def get_example_params():
    for py_file, cmd, output in get_examples():
        cmds = cmd.split()
        cmds.pop(0)
        cmds.pop(0)
        cmds.insert(0, py_file.name)
        yield param(py_file, cmd, output, id="-".join(cmds).replace(".", "_"))


# parameterize tests from examples directory
def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == "test_example":
        metafunc.parametrize("pyfile, cmd, expected", get_example_params())
