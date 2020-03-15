import log


def google_doc(param1: int, param2: str, kw1=None, kw2=False):
    """Example function with types documented in the docstring.

    Args:
        param1 (int): The first parameter.
        param2: The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    log.info(f"Got params: {param1}, {param2}, {kw1}, {kw2}")


def rest_doc():
    """Set the temperature value.

    The value of the temp parameter is stored as a value in
    the class variable temperature. The given value is converted
    into a float value if not yet done.

    :param temp: the temperature value
    :param empty:
    :param arg2: the temperature value multi line string
    to the third line
    :param arg3: just one line
    :type temp: float
    :return: no value
    :rtype: none
    """
