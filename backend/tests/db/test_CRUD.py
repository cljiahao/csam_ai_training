import pytest
from sqlalchemy.orm import Session

from db.CRUD.example import create_example, get_example, update_example
from db.models.example import EXAMPLE


@pytest.mark.parametrize("sample_example", ("example", ""))
def test_create_and_get_example(
    db_session: Session,
    sample_example: str,
) -> None:
    """Test the creation and retrieval of lot detail."""

    # Prepare test data
    created_detail = create_example(EXAMPLE, db_session, {"example": sample_example})

    # Retrieve the detail to verify creation
    example = get_example(EXAMPLE, db_session, sample_example)

    # Ensure the created detail matches the retrieved detail
    assert example is not None
    assert created_detail == example


@pytest.mark.parametrize("sample_example", ("example", ""))
def test_update_example(
    db_session: Session,
    sample_example: dict[str, str],
) -> None:
    """Test the update of lot detail."""

    # Prepare test data
    create_example(EXAMPLE, db_session, {"example": sample_example})

    new_example = "example2"
    updated_detail = update_example(EXAMPLE, db_session, 1, new_example)

    assert updated_detail is not None
    assert updated_detail.example == new_example
