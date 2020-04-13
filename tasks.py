from arger import Arger
from delegator import run

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
    END = '\033[0m'


def prun(*cmd, **kwargs):
    cmd = " ".join(cmd)
    print(f'{Color.OKGREEN} $ {cmd}{Color.END}')
    c = run(cmd, **kwargs)
    print(c.out)
    print(c.err)
    return c


@arger.add_cmd
def release(type: str):
    """Bump version, tag and push them.

    # todo: create an Enum
    :param type: one of patch, minor, major, prepatch, preminor, premajor, prerelease. as supported by poetry version
    """
    prun('poetry', 'version', type)
    c = prun('poetry', 'version')
    _, version = c.out.split()
    prun('git status')
    msg = 'chore: bump version'

    answer = input(f'{msg}\nAdd to commit: [Y/n]?')
    if answer.lower() in {'no', 'n'}:
        return
    prun('git add .')
    prun(f'git commit -m "{msg}"')
    prun(f'git tag v{version}')
    prun('git push')
    prun('git push --tags')


if __name__ == '__main__':
    arger.run()