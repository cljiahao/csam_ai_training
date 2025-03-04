from sqlalchemy.orm import Session

from constants.tf_model import ClassLabel
from core.exceptions import InvalidInputError
from db.models.base_sets import BaseSets
from db.repository.base_sets import BaseSetsRepository


class BaseSetsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.base_sets_repo = BaseSetsRepository(db)

    def _read_base_sets(self, item: str) -> BaseSets:
        """Service layer method to read base sets"""
        filter_condition = {"item": item}

        return self.base_sets_repo.read_base_sets(filter_condition)

    def create_or_update_base_sets(
        self, item: str, base_sets_data: dict[str, int]
    ) -> BaseSets:
        """Service layer method to create new or update base sets"""
        if not item:
            raise InvalidInputError()
        if set(base_sets_data) - set([c.value for c in ClassLabel]):
            raise InvalidInputError()

        data_condition = {"item": item}
        new_base_sets_data = {
            f"no_of_{k.lower()}": v for k, v in base_sets_data.items()
        }

        if not self._read_base_sets(item):
            new_base_sets_data.update(data_condition)
            return self.base_sets_repo.create_base_sets(new_base_sets_data)

        return self.base_sets_repo.update_base_sets(data_condition, new_base_sets_data)
