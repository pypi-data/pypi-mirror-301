from typing import Any, cast

from d42.declaration import SchemaVisitor
from d42.declaration import SchemaVisitorReturnType as ReturnType
from d42.declaration.types import ListSchema

__all__ = ("UnorderedSchema",)


class UnorderedSchema(ListSchema):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return cast(ReturnType, visitor.visit_unordered(self, **kwargs))
