import random
from typing import Any, cast

from d42.declaration import Props, Schema, SchemaVisitor
from d42.declaration import SchemaVisitorReturnType as ReturnType
from d42.declaration.errors import make_already_declared_error, make_invalid_type_error
from d42.generation import Generator
from d42.representation import Representor
from d42.substitution import Substitutor
from d42.substitution.errors import make_substitution_error
from d42.validation import ValidationResult, Validator
from d42.validation.errors import ValueValidationError
from niltype import Nil, Nilable
from th import PathHolder

__all__ = ("IStrSchema", "IStrProps",
           "IStrRepresentor", "IStrGenerator", "IStrValidator", "IStrSubstitutor",)


class IStrProps(Props):
    @property
    def value(self) -> Nilable[str]:
        return self.get("value")


class IStrSchema(Schema[IStrProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return cast(ReturnType, visitor.visit_istr(self, **kwargs))

    def __call__(self, /, value: str) -> "IStrSchema":
        if not isinstance(value, str):
            raise make_invalid_type_error(self, value, (str,))

        if self.props.value is not Nil:
            raise make_already_declared_error(self)

        return self.__class__(self.props.update(value=value))


class IStrRepresentor(Representor, extend=True):
    def visit_istr(self, schema: IStrSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.istr"
        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"
        return r


class IStrGenerator(Generator, extend=True):
    def visit_istr(self, schema: IStrSchema, **kwargs: Any) -> str:
        if schema.props.value is not Nil:
            modifier = random.choice((str, str.lower, str.upper))
            return modifier(schema.props.value)
        return ""


class IStrValidator(Validator, extend=True):
    def visit_istr(self, schema: IStrSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, str):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if value.lower() != schema.props.value.lower():
                error = ValueValidationError(path, value, schema.props.value)
                return result.add_error(error)

        return result


class IStrSubstitutor(Substitutor, extend=True):
    def visit_istr(self, schema: IStrSchema, *,
                   value: Any = Nil, **kwargs: Any) -> IStrSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))
