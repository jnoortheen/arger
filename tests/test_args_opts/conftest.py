# pylint: disable = redefined-outer-name, protected-access

import inspect

import pytest

from arger import Arger, Argument
from arger.docstring import ParamDocTp
from arger.main import FlagsGenerator


@pytest.fixture
def param_doc(hlp=""):
    return ParamDocTp.init("", hlp)


@pytest.fixture
def add_arger():
    def _add(argument):
        par = Arger()
        argument.add_to(par)
        return par

    return _add


@pytest.fixture
def gen_options():
    return FlagsGenerator("-")


@pytest.fixture
def parameter(name, tp):
    return inspect.Parameter(
        name,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        annotation=tp,
    )


@pytest.fixture
def argument(parameter, param_doc, gen_options) -> Argument:
    return Argument.create(parameter, param_doc, gen_options)


@pytest.fixture
def parser(add_arger, argument):
    return add_arger(argument)
