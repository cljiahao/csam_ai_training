from sqlalchemy.orm import Session

from constants.tf_model import ClassLabel
from core.exceptions import InvalidInputError
from db.models.base_sets import BaseSets
from db.repository.base_sets import BaseSetsRepository


class BaseSetsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = BaseSetsRepository(db)

    def _validate_base_sets_keys(self, base_sets_data: dict) -> None:
        """Validate the keys in the image settings data."""
        valid_keys = set([c.value for c in ClassLabel])

        invalid_keys = set(base_sets_data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in image settings data: {', '.join(invalid_keys)}"
            )

    def read_base_sets(self, item: str) -> BaseSets:
        """Service layer method to read base sets"""
        if not item:
            raise InvalidInputError("Filter conditions: Item cannot be empty.")
        filter_condition = {"item": item}

        return self.repo.read_base_sets(filter_condition)

    def create_or_update_base_sets(
        self, item: str, base_sets_data: dict[str, int]
    ) -> BaseSets:
        """Service layer method to create new or update base sets"""
        if not item:
            raise InvalidInputError("Filter conditions: Item cannot be empty.")

        self._validate_base_sets_keys(base_sets_data)

        data_condition = {"item": item}
        new_base_sets_data = {
            f"no_of_{k.lower()}": v for k, v in base_sets_data.items()
        }

        existing_base_sets = self.read_base_sets(item)
        if not existing_base_sets:
            new_base_sets_data.update(data_condition)
            return self.repo.create_base_sets(new_base_sets_data)

        return self.repo.update_base_sets(data_condition, new_base_sets_data)
