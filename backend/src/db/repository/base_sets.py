from sqlalchemy.orm import Session

from db.models.base_sets import BaseSets
from db.repository.base_repository import BaseRepository


class BaseSetsRepository(BaseRepository[BaseSets]):
    def __init__(self, db: Session):
        super().__init__(db, BaseSets)

    def create_base_sets(self, base_sets_data: dict) -> list[BaseSets]:
        """Create new base sets."""
        return self.create(
            base_sets_data,
            print_message="Error creating new data into BaseSets database.",
        )

    def read_all_base_sets(self, filter_conditions: dict) -> list[BaseSets]:
        """Read all base sets based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading all data from BaseSets database.",
        )

    def read_base_sets(self, filter_conditions: dict) -> list[BaseSets]:
        """Read base sets based on filter."""
        return self.read(
            filter_conditions,
            print_message="Error reading data from BaseSets database.",
        )

    def update_base_sets(self, update_lists: list[dict[str, dict]]) -> int:
        """Update base sets with provided data."""
        return self.update(
            update_lists, print_message="Error updating data in BaseSets database."
        )

    def delete_base_sets(self, filter_conditions: dict) -> int:
        """Delete base sets based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from BaseSets database.",
        )
