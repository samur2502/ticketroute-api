from datetime import UTC, datetime
from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter

from ticketroute.schemas.predictions import (
    PredictionRequest,
    PredictionResponse,
)

router = APIRouter(prefix="/v1/predictions", tags=["predictions"])


@router.post("", response_model=PredictionResponse, status_code=HTTPStatus.CREATED)
def create_prediction(request: PredictionRequest) -> PredictionResponse:
    return PredictionResponse(
        id=uuid4(),
        intent="unclassified",
        confidence=0.0,
        alternatives=[],
        needs_review=True,
        model_version="no_model",
        latency_ms=0,
        created_at=datetime.now(UTC),
    )
