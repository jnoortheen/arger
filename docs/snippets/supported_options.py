from enum import Enum
from typing import List

from arger import Arger
from tests.utils import _reprint


class Choice(Enum):
    one = '1. One'
    two = '2. Two'


arger = Arger(prog='pytest', description="App Description goes here")

container = []


@arger.add_cmd
def varargs(
    an_int: int,
    an_str: str,
    a_tuple: List[str, str, str],
    a_var_tuple: List[str, ...],
    a_list: List[int],
    an_enum=Enum.one,
    optional_str='',
    optional_int=0,
    optional_tpl=(),
):
    """Example function with types documented in the docstring."""
    _reprint(**locals())


@arger.add_cmd
def optstring3(m_opt=False, y_opt=False, my=False):
    """A script with three optional values, no short option left for last value.
    :param m_opt: the m_opt helptext
    :param y_opt: the y_opt helptext
    :param my: the my helptext
    """
    _reprint(**locals())


def optstring2(myoption=False, mysecondoption=False):
    """A script with two optional values.
    :param myoption: the myoption helptext
    :param secondoption: the second helptext
    """
    _reprint(**locals())


if __name__ == '__main__':
    arger.run()
