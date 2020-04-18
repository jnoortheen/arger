from typing import Any, List, Tuple

from pytest import fixture, mark
from pytest_lazyfixture import lazy_fixture as lz

from arger.typing_utils import get_origin, match_types


@fixture(params=[list, List, List[str], List[int], List[Any]])
def list_type(request):
    return request.param


@fixture(
    params=[tuple, Tuple, Tuple[str], Tuple[str, str], Tuple[int], Tuple[int, ...]]
)
def tuple_type(request):
    return request.param


@mark.parametrize(
    "tp, tps, expected",
    [
        (lz("list_type"), lz("list_type"), True),
        (lz("list_type"), lz("tuple_type"), False),
        (lz("tuple_type"), lz("tuple_type"), True),
        (lz("tuple_type"), lz("list_type"), False),
    ],
)
def test_match_types(tp, tps, expected):
    assert match_types(tp, tps) == expected


@mark.parametrize("tp, expected", [(lz("list_type"), list), (lz("tuple_type"), tuple),])
def test_get_origin(tp, expected):
    assert get_origin(tp) == expected
