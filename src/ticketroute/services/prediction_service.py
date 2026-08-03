from dataclasses import dataclass
from datetime import UTC, datetime
from time import perf_counter_ns
from uuid import UUID, uuid4

from ticketroute.ml.classifier import Classification, classify

CONFIDENCE_THRESHOLD = 0.65
MODEL_VERSION = "keyword_rules_v1"


@dataclass(frozen=True)
class Prediction:
    id: UUID
    intent: str
    confidence: float
    alternatives: tuple[Classification, ...]
    needs_review: bool
    model_version: str
    latency_ms: int
    created_at: datetime


def predict_message(text: str, top_k: int) -> Prediction:
    started_at = perf_counter_ns()

    classifications = classify(text, top_k)

    latency_ms = (perf_counter_ns() - started_at) // 1_000_000

    primary = classifications[0]
    alternatives = tuple(classifications[1:])

    return Prediction(
        id=uuid4(),
        intent=primary.intent,
        confidence=primary.confidence,
        alternatives=alternatives,
        needs_review=primary.confidence < CONFIDENCE_THRESHOLD,
        model_version=MODEL_VERSION,
        latency_ms=latency_ms,
        created_at=datetime.now(UTC),
    )
