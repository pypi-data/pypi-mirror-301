from baby_steps import given, then, when
from d42.representation import represent

from jj_d42.types.param_list import ParamListSchema


def test_param_list_representation():
    with given:
        sch = ParamListSchema()

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "ParamListSchema<schema.unordered(schema.list([",
            "    schema.str,",
            "    schema.str",
            "]))>",
        ])
