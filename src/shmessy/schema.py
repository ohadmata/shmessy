from typing import Any, List, Optional

from pydantic import BaseModel


class BaseField(BaseModel):
    field_name: str
    source_type: str


class InferredField(BaseModel):
    inferred_type: Optional[str] = None
    inferred_pattern: Optional[Any] = None


class Field(InferredField, BaseField):
    pass


class ShmessySchema(BaseModel):
    columns: List[Field]
    infer_duration_ms: int
