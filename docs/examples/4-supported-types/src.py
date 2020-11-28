from enum import Enum
from typing import List, Tuple

from arger import Arger
from tests.utils import _reprint


class Choice(Enum):
    one = '1. One'
    two = '2. Two'


arger = Arger(prog='pytest', description="App Description goes here")

container = []


@arger.add_cmd
def cmd1(
    an_int: int,
    an_str: str,
    a_tuple: Tuple[str, str, str],  # nargs: 3 -> consume 3
    a_var_tuple: Tuple[str, ...],  # nargs: +  -> consume one or more
    an_enum=Choice.one,
    optional_str='',
    optional_int=0,
    optional_tpl=(),
):
    """Example function with types documented in the docstring."""
    _reprint(**locals())


@arger.add_cmd
def cmd2(
    a_list: List[int],  # nargs='*': -> capture many args
    m_opt=False,
    y_opt=False,
    my=False,
):
    """A script with three optional values.

    :param a_list: catch all positional arguments
    :param m_opt: the m_opt helptext
    :param y_opt: the y_opt helptext
    :param my: the my helptext
    """
    _reprint(**locals())


if __name__ == '__main__':
    arger.run()
