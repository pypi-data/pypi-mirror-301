from baby_steps import given, then, when
from d42 import fake

from jj_d42.types.param_list import ParamListSchema


def test_param_list_generation():
    with given:
        sch = ParamListSchema()

    with when:
        res = fake(sch)

    with then:
        assert isinstance(res, list)
