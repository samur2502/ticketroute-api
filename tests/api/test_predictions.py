from datetime import datetime
from http import HTTPStatus
from uuid import UUID

import pytest
from fastapi.testclient import TestClient


def test_create_prediction(client: TestClient) -> None:
    response = client.post(
        "/v1/predictions",
        json={"text": "I forgot my PIN"},
    )

    assert response.status_code == HTTPStatus.CREATED

    body = response.json()

    assert UUID(body["id"]).version == 4
    assert body["intent"] == "forgotten_pin"
    assert body["confidence"] == 1.0
    assert body["alternatives"] == [
        {
            "intent": "change_pin",
            "confidence": 0.5,
        }
    ]
    assert body["needs_review"] is False
    assert body["model_version"] == "keyword_rules_v1"
    assert body["latency_ms"] >= 0

    created_at = datetime.fromisoformat(body["created_at"])
    assert created_at.tzinfo is not None


@pytest.mark.parametrize(
    "payload",
    [
        {"text": ""},
        {"text": "    "},
        {"text": "I forgot my PIN", "top_k": 0},
        {"text": "I forgot my PIN", "top_k": 6},
        {"text": "I forgot my PIN", "topk": 2},
        {"text": "I forgot my PIN", "random_field": True},
        {"text": "a" * 2_001},
    ],
)
def test_create_prediction_rejects_invalid_request(
    client: TestClient, payload: dict[str, object]
) -> None:
    response = client.post("/v1/predictions", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]


def test_create_prediction_uses_top_k(client: TestClient) -> None:
    response = client.post(
        "/v1/predictions",
        json={"text": "I forgot my PIN!", "top_k": 1},
    )

    assert response.status_code == HTTPStatus.CREATED

    body = response.json()

    assert body["intent"] == "forgotten_pin"
    assert body["alternatives"] == []
