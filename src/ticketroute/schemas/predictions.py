from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

PredictionText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=2_000,
    ),
]


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: PredictionText
    top_k: int = Field(default=3, ge=1, le=5)


class PredictionAlternative(BaseModel):
    intent: str
    confidence: float = Field(ge=0.0, le=1.0)


class PredictionResponse(BaseModel):
    id: UUID
    intent: str
    confidence: float = Field(ge=0.0, le=1.0)
    alternatives: list[PredictionAlternative]
    needs_review: bool
    model_version: str
    latency_ms: int = Field(ge=0)
    created_at: datetime
