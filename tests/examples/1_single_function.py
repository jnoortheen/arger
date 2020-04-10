import arger
from tests.utils import _reprint


def main(param1: int, param2: str, kw1=None, kw2=False):
    """Example function with types documented in the docstring.

    :param param1: The first parameter.
    :param param2: The second parameter.
    """
    _reprint(**locals())


if __name__ == '__main__':
    arger.run(main)
