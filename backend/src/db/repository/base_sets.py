from sqlalchemy.orm import Session

from db.models.base_sets import BaseSets
from db.repository.base_repository import BaseRepository


class BaseSetsRepository(BaseRepository[BaseSets]):
    def __init__(self, db: Session):
        super().__init__(db, BaseSets)

    def create_base_sets(self, base_sets_data: dict) -> BaseSets:
        """Create new base sets."""
        return self.create(
            base_sets_data,
            print_message=f"Error creating base sets from the database.",
        )

    def read_base_sets(self, filter_condition: dict) -> BaseSets:
        """Read base sets based on filter."""
        return self.read(
            filter_condition,
            print_message=f"Error reading base sets from the database.",
        )

    def update_base_sets(self, filter_condition: dict, update_data: dict) -> BaseSets:
        """Update base sets with provided data."""
        return self.update(
            filter_condition,
            update_data,
            print_message=f"Error updating base sets in the database.",
        )

    def delete_base_sets(self, filter_condition: dict) -> BaseSets:
        """Delete base sets based on filter."""
        return self.delete(
            filter_condition,
            print_message=f"Error deleting base sets from the database.",
        )
