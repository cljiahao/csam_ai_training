import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def sample_example() -> str:
    return {"example": "example"}


def test_get_example_success(
    test_client: TestClient,
    sample_example: dict[str, str],
) -> None:
    """Test example route."""

    response = test_client.get("/v1/example/example")

    assert response.status_code == 200
    assert response.json() == sample_example


def test_get_example_exception(
    test_client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test example route exception."""

    mock_component_example = MagicMock()
    mock_component_example.side_effect = Exception("Unexpected Error.")
    monkeypatch.setattr(
        "apis.v2.routers.example.component_example", mock_component_example
    )

    response = test_client.get("/v1/example/example")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Bad Request: The request was invalid or cannot be served."
    }


def test_get_example_invalid(
    test_client: TestClient,
) -> None:
    """Test invalid example route."""

    response = test_client.get("/v1/example/ex")

    assert response.status_code == 422
