from delegator import run
from subprocess import check_output
from arger import Arger, Option

arger = Arger(description="Common set of tasks to run")


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # reset
    RESET = '\033[0m'


def prun(*cmd, **kwargs):
    cmd = " ".join(cmd)
    print(f'{Color.OKGREEN} $ {cmd}{Color.RESET}')
    c = run(cmd, **kwargs)
    print(c.out)
    print(c.err)
    return c


@arger.add_cmd
def release(
    type: str = Option(
        choices=[
            'patch',
            'minor',
            'major',
            'prepatch',
            'preminor',
            'premajor',
            'prerelease',
        ],
        default='patch',
        action='store',
    )
):
    """Bump version, tag and push them.

    Args:
        type: version bump as supported by `poetry version` command
    """
    prun('poetry', 'version', type)
    c = prun('poetry', 'version')
    _, version = c.out.split()

    version_num = f"v{version}"
    prun('cz', 'changelog', '--unreleased-version', version_num)
    prun('git status')
    msg = 'chore: bump version'

    answer = input(f'{msg}\nAdd to commit: [Y/n]?')
    if answer.lower() in {'no', 'n'}:
        return
    prun('git add .')
    prun(f'git commit -m "{msg}"')
    prun(f'git tag {version_num}')
    prun('git push')
    prun('git push --tags')
    prun('mkdocs gh-deploy')


# @arger.add_cmd
# def test():
#     print('run tests')


@arger.add_cmd
def show_coverage():
    out = check_output(["coverage", "report"])
    total = out.decode().splitlines()[-1]
    assert "total" in total.lower()
    print(total.split()[-1])


if __name__ == '__main__':
    arger.run()
