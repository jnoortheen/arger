import inspect

import pytest

from arger import Arger, Argument, Option
from arger.docstring import ParamDocTp
from arger.funcs import _EMPTY, FlagsGenerator, create_argument, create_option


@pytest.fixture
def param_doc(hlp=''):
    return ParamDocTp.init('', hlp)


@pytest.fixture
def parameter(name, tp=_EMPTY, default=_EMPTY):
    return inspect.Parameter(
        name,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        annotation=tp,
        default=default,
    )


@pytest.fixture
def argument(parameter, param_doc) -> Argument:
    return create_argument(parameter, param_doc)


@pytest.fixture
def add_arger():
    def _add(argument):
        par = Arger()
        argument.add(par)
        return par

    return _add


@pytest.fixture
def gen_options():
    return FlagsGenerator()


@pytest.fixture
def option(parameter, param_doc, gen_options) -> Option:
    return create_option(parameter, param_doc, gen_options)
