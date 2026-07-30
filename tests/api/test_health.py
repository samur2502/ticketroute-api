from http import HTTPStatus

from fastapi.testclient import TestClient

from ticketroute.main import app


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "status": "unhealthy",
        "model_loaded": False,
        "database_connected": False,
    }
