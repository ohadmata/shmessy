from enum import Enum
from typing import List, Optional, Type

from pydantic import BaseModel


class ValidatorTypes(str, Enum):
    NUMERIC = "NUMERIC"
    STRING = "STRING"


class BaseField(BaseModel):
    field_name: str
    source_type: Type


class InferredField(BaseModel):
    inferred_type: Optional[Type] = None
    inferred_virtual_type: Optional[Type] = None
    inferred_pattern: Optional[str] = None


class Field(InferredField, BaseField):
    pass


class ShmessySchema(BaseModel):
    columns: List[Field]
    infer_duration_ms: int
