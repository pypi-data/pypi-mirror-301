from baby_steps import given, then, when
from d42.generation import generate
from jj.mock import HistoryResponse

from jj_d42 import HistoryResponseSchema


def test_history_response_generation():
    with given:
        sch = HistoryResponseSchema()

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, HistoryResponse)
