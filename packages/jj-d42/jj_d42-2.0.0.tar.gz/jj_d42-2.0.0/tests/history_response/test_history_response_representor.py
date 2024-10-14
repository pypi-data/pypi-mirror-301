from baby_steps import given, then, when
from d42.representation import represent

from jj_d42 import HistoryResponseSchema


def test_history_response_representation():
    with given:
        sch = HistoryResponseSchema()

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "HistoryResponseSchema<schema.dict({",
            "    'status': schema.int,",
            "    'reason': schema.str,",
            "    'headers': HeaderListSchema<schema.unordered(schema.list([",
            "        schema.istr,",
            "        schema.str",
            "    ]))>,",
            "    'body': schema.any,",
            "    'raw': schema.bytes",
            "})>",
        ])
