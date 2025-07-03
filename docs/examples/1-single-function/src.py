from argparse import Namespace

from arger import Arger
from tests.utils import _reprint


def main(param1: int, param2: str, _namespace_: Namespace, kw1=None, kw2=False):
    """Example function with types documented in the docstring.

    :param param1: The first parameter.
    :param param2: The second parameter.
    :param kw1: this is optional parameter.
    :param kw2: this is boolean. setting flag sets True.
    """
    _reprint(**locals())


arger = Arger(
    main,
    prog="pytest",  # for testing purpose. otherwise not required
)

if __name__ == "__main__":
    arger.run()
