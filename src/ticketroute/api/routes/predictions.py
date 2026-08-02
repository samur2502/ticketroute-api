from http import HTTPStatus

from fastapi import APIRouter

from ticketroute.schemas.predictions import (
    PredictionAlternative,
    PredictionRequest,
    PredictionResponse,
)
from ticketroute.services.prediction_service import predict_message

router = APIRouter(prefix="/v1/predictions", tags=["predictions"])


@router.post("", response_model=PredictionResponse, status_code=HTTPStatus.CREATED)
def create_prediction(request: PredictionRequest) -> PredictionResponse:
    prediction = predict_message(
        request.text,
        request.top_k,
    )
    return PredictionResponse(
        id=prediction.id,
        intent=prediction.intent,
        confidence=prediction.confidence,
        alternatives=[
            PredictionAlternative(
                intent=alternative.intent,
                confidence=alternative.confidence,
            )
            for alternative in prediction.alternatives
        ],
        needs_review=prediction.needs_review,
        model_version=prediction.model_version,
        latency_ms=prediction.latency_ms,
        created_at=prediction.created_at,
    )
