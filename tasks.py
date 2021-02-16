from delegator import run
from typing_extensions import Literal

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
    cmd = " ".join(cmd)
    print(f"{Color.OKGREEN} $ {cmd}{Color.RESET}")
    c = run(cmd, **kwargs)
    print(c.out)
    print(c.err)
    return c


@arger.add_cmd
def release(
    type: Literal[
                "patch",
                "minor",
                "major",
                "prepatch",
                "preminor",
                "premajor",
                "prerelease",
            ]
    = "patch"
):
    """Bump version, tag and push them.

    Args:
        type: version bump as supported by `poetry version` command
    """
    prun("make", "check", "test")
    prun("poetry", "version", type)
    c = prun("poetry", "version")
    _, version = c.out.split()

    version_num = f"v{version}"
    msg = f"chore: bump version to {version_num}"

    # tagging the current commit in order to place the name correct in the changelog
    prun(f"git tag {version_num}")

    prun("git-changelog", ".", "-s", "angular", "-o", "CHANGELOG.md")
    prun("git status")

    answer = input(f"{msg}\nAdd to commit: [Y/n]?")
    if answer.lower() in {"no", "n"}:
        return
    prun("git add .")
    prun(f'git commit -m "{msg}"')

    # using force to move the tag to the latest commit.
    prun(f"git tag {version_num} --force")

    prun("git push")
    prun("git push --tags")


# @arger.add_cmd
# def test():
#     print('run tests')


class Devnull(object):
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


if __name__ == "__main__":
    arger.run()
