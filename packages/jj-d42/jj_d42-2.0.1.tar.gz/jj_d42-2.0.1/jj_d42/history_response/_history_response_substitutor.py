from typing import Any, cast

from d42.substitution import Substitutor, SubstitutorValidator
from d42.validation import ValidationResult
from jj.mock import HistoryResponse
from niltype import Nil, Nilable
from th import PathHolder

from ._history_response_schema import HistoryResponseSchema

__all__ = ("HistoryResponseSubstitutor", "HistoryResponseSubstitutorValidator",)


class HistoryResponseSubstitutor(Substitutor, extend=True):
    def visit_jj_history_response(self, schema: HistoryResponseSchema, *,
                                  value: Any = Nil, **kwargs: Any) -> HistoryResponseSchema:
        if isinstance(value, HistoryResponse):
            value = value.to_dict()
        return cast(HistoryResponseSchema, self.visit_type_alias(schema, value=value, **kwargs))


class HistoryResponseSubstitutorValidator(SubstitutorValidator, extend=True):
    def visit_jj_history_response(self, schema: HistoryResponseSchema, *,
                                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                                  **kwargs: Any) -> ValidationResult:
        if isinstance(value, HistoryResponse):
            value = value.to_dict()
        return self.visit_type_alias(schema, value=value, path=path, **kwargs)
