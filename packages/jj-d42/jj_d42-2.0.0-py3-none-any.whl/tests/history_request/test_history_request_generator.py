from baby_steps import given, then, when
from d42.generation import generate
from jj.mock import HistoryRequest

from jj_d42 import HistoryRequestSchema


def test_history_request_generation():
    with given:
        sch = HistoryRequestSchema()

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, HistoryRequest)
