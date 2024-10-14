from baby_steps import given, then, when
from d42.representation import represent

from jj_d42.types.header_list import HeaderListSchema


def test_header_list_representation():
    with given:
        sch = HeaderListSchema()

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "HeaderListSchema<schema.unordered(schema.list([",
            "    schema.istr,",
            "    schema.str",
            "]))>",
        ])
