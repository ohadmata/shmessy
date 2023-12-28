from pydantic import BaseModel
from typing import Optional, List, Any
from enum import Enum


class ValidatorTypes(str, Enum):
    NUMERIC = "NUMERIC"
    STRING = "STRING"


class BaseField(BaseModel):
    field_name: str
    source_type: str


class InferredField(BaseModel):
    inferred_type: Optional[str] = None
    inferred_virtual_type: Optional[Any] = None
    inferred_pattern: Optional[str] = None


class Field(InferredField, BaseField):
    pass


class ShmessyMetadata(BaseModel):
    metadata: List[Field]
