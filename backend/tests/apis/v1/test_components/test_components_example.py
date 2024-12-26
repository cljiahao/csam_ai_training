import pytest
from sqlalchemy.orm import Session

from apis.v2.components.example import component_example


@pytest.fixture
def sample_example() -> str:
    return "example"


def test_component_example(sample_example: str, db_session: Session) -> None:

    result = component_example(sample_example, db_session)

    assert result == {"example": sample_example}
