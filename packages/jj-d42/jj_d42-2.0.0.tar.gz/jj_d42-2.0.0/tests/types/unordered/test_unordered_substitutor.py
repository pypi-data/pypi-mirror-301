from typing import Any, List

import pytest
from baby_steps import given, then, when
from d42 import schema, substitute

from jj_d42.types.unordered import unordered_schema


@pytest.mark.parametrize("value", [
    [],
    [1],
    [1, 2],
])
def test_unordered_elements_substitution(value: List[Any]):
    with given:
        sch = unordered_schema

    with when:
        res = substitute(sch, value)

    with then:
        assert res == unordered_schema([substitute(schema.int, x) for x in value])
        assert res != sch
