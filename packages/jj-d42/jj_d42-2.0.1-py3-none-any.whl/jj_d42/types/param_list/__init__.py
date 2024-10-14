from typing import Any, cast

from d42 import schema as sch
from d42.declaration import SchemaVisitor
from d42.declaration import SchemaVisitorReturnType as ReturnType
from d42.declaration.types import DictSchema, GenericTypeAliasSchema, TypeAliasProps
from d42.substitution import Substitutor
from d42.validation import ValidationResult, Validator
from niltype import Nil, Nilable
from th import PathHolder

from jj_d42.types.unordered import unordered_schema

__all__ = ("ParamListSchema", "ParamListProps",
           "ParamListSubstitutor", "ParamListValidator",)


class ParamListProps(TypeAliasProps):
    @property
    def type(self) -> DictSchema:
        key_val = sch.list([sch.str, sch.str])
        type_ = self.get("type", unordered_schema(key_val))
        return cast(DictSchema, type_)


class ParamListSchema(GenericTypeAliasSchema[ParamListProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        try:
            return cast(ReturnType, visitor.visit_jj_param_list(self, **kwargs))
        except AttributeError:
            return visitor.visit_type_alias(self, **kwargs)


class ParamListSubstitutor(Substitutor, extend=True):
    def visit_jj_param_list(self, schema: ParamListSchema, *,
                            value: Any = Nil, **kwargs: Any) -> ParamListSchema:
        if isinstance(value, dict):
            value = [[key, val] for key, val in value.items()]
        return cast(ParamListSchema, self.visit_type_alias(schema, value=value, **kwargs))


class ParamListValidator(Validator, extend=True):
    def visit_jj_param_list(self, schema: ParamListSchema, *,
                            value: Any = Nil, path: Nilable[PathHolder] = Nil,
                            **kwargs: Any) -> ValidationResult:
        if isinstance(value, dict):
            value = [[key, val] for key, val in value.items()]
        return self.visit_type_alias(schema, value=value, path=path, **kwargs)
