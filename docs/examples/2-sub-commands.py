from arger import Arger
from tests.utils import _reprint

arger = Arger(prog="pytest", description="App Description goes here")

container = []


@arger.add_cmd
def create(name: str):
    """Create new test.

    :param name: Name of the test
    """
    container.append(container)
    _reprint(**locals())


@arger.add_cmd
def remove(*name: str):
    """Remove a test with variadic argument.

    :param name: tests to remove
    """
    if name in container:
        container.remove(remove)
    _reprint(**locals())


@arger.add_cmd
def list():
    """List all tests."""
    _reprint(**locals(), container=container)


if __name__ == "__main__":
    arger.run()
