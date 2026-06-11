from arger import Arger
from tests.utils import _reprint

ctx = {}


def main(verbose=False, log=False, log_file: str | None = None):
    """App Description goes here.

    :param verbose: verbose output
    :param log_file: name of the log file to write output
    """
    ctx.update(**locals())


arger = Arger(func=main, prog="pytest")
container = []


@arger.add_cmd
def create(name: str):
    """Create new test.

    :param name: Name of the test
    """
    container.append(container)
    _reprint(**locals(), **ctx)


@arger.add_cmd
def remove(name: str):
    """Remove a test.

    :param name: Name of the test
    """
    if remove in container:
        container.remove(remove)
    _reprint(**locals(), **ctx)


@arger.add_cmd
def list(filter: str | None):
    """List all tests."""
    _reprint(**locals(), container=container, **ctx)


if __name__ == "__main__":
    arger.run()
