from datetime import datetime
from http import HTTPStatus
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from ticketroute.main import app


def test_create_prediction() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/v1/predictions",
            json={"text": "I forgot my PIN"},
        )

    assert response.status_code == HTTPStatus.CREATED

    body = response.json()

    assert UUID(body["id"]).version == 4
    assert body["intent"] == "unclassified"
    assert body["confidence"] == 0.0
    assert body["alternatives"] == []
    assert body["needs_review"] is True
    assert body["model_version"] == "no_model"
    assert body["latency_ms"] == 0

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
def test_create_prediction_rejects_invalid_request(payload: dict[str, object]) -> None:
    with TestClient(app) as client:
        response = client.post("/v1/predictions", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"]
