from baby_steps import then, when

from jj_d42.types.unordered import UnorderedSchema, unordered_schema


def test_unordered_declaration():
    with when:
        sch = unordered_schema

    with then:
        assert isinstance(sch, UnorderedSchema)
