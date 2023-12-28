from enum import Enum
from typing import Optional, List
from typing import Type

from pydantic import BaseModel, field_serializer


class ValidatorTypes(str, Enum):
    NUMERIC = "NUMERIC"
    STRING = "STRING"


class BaseField(BaseModel):
    field_name: str
    source_type: Type

    @field_serializer('source_type')
    def serialize_source_type(self, source_type: Type, _info):
        return str(source_type)


class InferredField(BaseModel):
    inferred_type: Optional[Type] = None
    inferred_virtual_type: Optional[Type] = None
    inferred_pattern: Optional[str] = None

    @field_serializer('inferred_type')
    def serialize_inferred_type(self, inferred_type: Type, _info):
        return str(inferred_type)

    @field_serializer('inferred_virtual_type')
    def serialize_inferred_virtual_type(self, inferred_virtual_type: Type, _info):
        return str(inferred_virtual_type)


class Field(InferredField, BaseField):
    pass


class ShmessySchema(BaseModel):
    columns: List[Field]
    infer_duration_ms: int
