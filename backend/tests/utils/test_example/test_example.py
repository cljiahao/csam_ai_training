import pytest
from unittest.mock import MagicMock

from utils.example.example import run_example


@pytest.fixture
def sample_example() -> str:
    return "example"


@pytest.fixture
def mock_logger(mock_func_logger: MagicMock) -> MagicMock:
    return mock_func_logger("utils.example.example.logger")


def test_example(sample_example: str, mock_logger: MagicMock) -> None:

    result = run_example(sample_example)

    assert result == sample_example
    mock_logger.info.assert_called_once_with(f"Received information {sample_example}")
