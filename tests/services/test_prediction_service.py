from datetime import UTC

import pytest

from ticketroute.ml.classifier import Classification
from ticketroute.services import prediction_service


def test_predict_message_builds_prediction() -> None:
    prediction = prediction_service.predict_message(
        text="I forgot my PIN",
        top_k=3,
    )

    assert prediction.id.version == 4
    assert prediction.intent == "forgotten_pin"
    assert prediction.confidence == 1.0
    assert prediction.alternatives == (
        Classification(intent="change_pin", confidence=0.5),
    )
    assert prediction.needs_review is False
    assert prediction.model_version == "keyword_rules_v1"
    assert prediction.latency_ms >= 0
    assert prediction.created_at.tzinfo is UTC


@pytest.mark.parametrize(
    ("confidence", "expected_needs_review"),
    [
        (0.64, True),
        (0.65, False),
    ],
)
def test_predict_message_applies_confidence_threshold(
    confidence: float,
    expected_needs_review: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def classify_stub(text: str, top_k: int) -> list[Classification]:
        return [
            Classification(
                intent="test_intent",
                confidence=confidence,
            ),
        ]

    monkeypatch.setattr(
        prediction_service,
        "classify",
        classify_stub,
    )

    prediction = prediction_service.predict_message(
        text="test message",
        top_k=1,
    )

    assert prediction.needs_review is expected_needs_review


def test_predict_message_measures_classifier_latency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    timestamps = iter(
        [
            1_000_000_000,
            1_042_000_000,
        ]
    )
    monkeypatch.setattr(
        prediction_service,
        "perf_counter_ns",
        lambda: next(timestamps),
    )

    prediction = prediction_service.predict_message(
        text="I forgot my PIN",
        top_k=1,
    )

    assert prediction.latency_ms == 42
