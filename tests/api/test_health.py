from http import HTTPStatus

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "status": "unhealthy",
        "model_loaded": False,
        "database_connected": False,
    }
