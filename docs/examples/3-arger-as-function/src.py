from typing import Optional

from arger import Arger
from tests.utils import _reprint

ctx = {}


@Arger.init(prog="pytest")  # any argument to the parser
def arger(verbose=False, log=False, log_file: Optional[str] = None):
    """App Description goes here.

    :param verbose: verbose output
    :param log_file: name of the log file to write output
    """
    ctx.update(**locals())


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
def list(filter: Optional[str]):
    """List all tests."""
    _reprint(**locals(), container=container, **ctx)


if __name__ == "__main__":
    arger.run()
