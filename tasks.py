# pylint: disable = subprocess-run-check,raising-bad-type,import-outside-toplevel,super-init-not-called
import shlex
import subprocess as sp
import sys

from arger import Arger

arger = Arger(
    description="Common set of tasks to run",
)


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # reset
    RESET = "\033[0m"


def prun(*cmd, **kwargs):
    if len(cmd) == 1 and len(shlex.split(cmd[0])) > 1:
        cmd = shlex.split(cmd[0])
    print(f"{Color.OKGREEN} $ {' '.join(cmd)}{Color.RESET}")
    c = sp.run(cmd, **kwargs, capture_output=True)
    sys.stdout.write(c.stdout.decode())
    sys.stdout.flush()
    sys.stderr.write(c.stderr.decode())
    sys.stderr.flush()
    if c.returncode:
        raise arger.exit(
            message=f"Failed[{c.returncode}] - {cmd}",
            status=c.returncode,
        )
    return c


class Devnull:
    """
    A file like object that does nothing.
    """

    def write(self, *args, **kwargs):
        pass


@arger.add_cmd
def show_coverage():
    import coverage

    class Precision(coverage.results.Numbers):
        """
        A class for using the percentage rounding of the main coverage package,
        with any percentage.
        To get the string format of the percentage, use the ``pc_covered_str``
        property.
        """

        def __init__(self, percent):
            self.percent = percent

        @property
        def pc_covered(self):
            return self.percent

    cov = coverage.Coverage()
    cov.load()
    total = cov.report(file=Devnull())
    print(Precision(total).pc_covered_str)


def _run_cmd(command):
    import subprocess

    run_command = command
    if run_command.startswith("python "):
        run_command = run_command.replace("python ", f'"{sys.executable}" ', 1)
    elif run_command.startswith("python3 "):
        run_command = run_command.replace("python3 ", f'"{sys.executable}" ', 1)
    try:
        result = subprocess.run(
            run_command,
            shell=True,
            text=True,
            capture_output=True,
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)


def process_markdown_file(md_path):
    content = md_path.read_text()
    lines = content.splitlines()
    new_lines = []

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.strip() == "```console":
            idx += 1
            if idx < len(lines):
                cmd_line = lines[idx]
                command = cmd_line[2:].strip() if cmd_line.startswith("$ ") else cmd_line.strip()

                idx += 1
                while idx < len(lines) and lines[idx].strip() != "```":
                    idx += 1

                output = _run_cmd(command)

                new_lines.append("```console")
                new_lines.append(f"$ {command}")
                new_lines.extend(output.splitlines())
                new_lines.append("```")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
        idx += 1

    md_path.write_text("\n".join(new_lines) + "\n")


@arger.add_cmd
def update_example_usage():
    """Run the cmd inside docs/examples/*.md and update their output"""
    from pathlib import Path

    examples_dir = Path("docs/examples")
    for md_path in examples_dir.glob("*.md"):
        print(f"Processing {md_path.name}...")
        process_markdown_file(md_path)


if __name__ == "__main__":
    arger.run()
