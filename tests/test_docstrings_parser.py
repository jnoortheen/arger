import pytest

from arger.docstring import DocstringParser, ParamDocTp


def func_numpy():
    """Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2
        a line that extends to next line
    arg3 :
        arg3 without any type
    arg4
        arg4 help content

    Returns
    -------
    bool
        Description of return value
    """


def func_google():
    """Summary line.

    Extended description of function.

    Args:
        arg1 (int): Description of arg1
        arg2 (str): Description of arg2
            a line that extends to next line
        arg3 : arg3 without any type
        arg4: arg4 help content

    Returns:
        bool: Description of return value
    """


# https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html
def func_rst():
    """Summary line.

    Extended description of function.

    :param int arg1: Description of arg1
    :param str arg2: Description of arg2
        a line that extends to next line
    :param arg3 : arg3 without any type
    :param arg4: arg4 help content
    :return: Description of return value
    :rtype: bool
    """


@pytest.mark.parametrize(
    "fn",
    [
        func_numpy,
        func_google,
        func_rst,
    ],
)
def test_docstring_parser(fn):
    result = DocstringParser.parse(fn)
    assert result.description == "Summary line.\n\nExtended description of function."
    assert list(result.params) == ["arg1", "arg2", "arg3", "arg4"]
    assert list(result.params.values()) == [
        ParamDocTp.init(
            type_hint="int",
            doc="Description of arg1",
        ),
        ParamDocTp.init(
            type_hint="str",
            doc="Description of arg2 a line that extends to next line",
        ),
        ParamDocTp.init(
            type_hint=None,
            doc="arg3 without any type",
        ),
        ParamDocTp.init(
            type_hint=None,
            doc="arg4 help content",
        ),
    ]
    assert "Description of return value" in result.epilog
