from baby_steps import given, then, when
from pytest import raises

from jj_district42.utils import contains


def test_contains_empty():
    with when, raises(Exception) as exception:
        assert contains({})

    with then:
        assert exception.type is ValueError


def test_contains_param():
    with given:
        params = {"Host": "localhost:8080"}

    with when:
        result = contains(params)

    with then:
        assert result == [..., ["Host", "localhost:8080"], ...]


def test_contains_params():
    with given:
        params = {
            "Host": "localhost:8080",
            "Content-Type": "application/json",
        }

    with when:
        result = contains(params)

    with then:
        assert result == [
            ...,
            ["Host", "localhost:8080"],
            ["Content-Type", "application/json"],
            ...
        ]
