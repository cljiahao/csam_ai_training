from sqlalchemy.orm import Session

from db.models.retrain_sets import ReTrainSets
from db.repository.base_repository import BaseRepository


class ReTrainSetsRepository(BaseRepository[ReTrainSets]):
    def __init__(self, db: Session):
        super().__init__(db, ReTrainSets)

    def create_retrain_sets(self, retrain_sets_data: dict) -> list[ReTrainSets]:
        """Create new re-train sets."""
        return self.create(
            retrain_sets_data,
            print_message="Error creating new data into ReTrainSets database.",
        )

    def read_all_retrain_sets(self, filter_conditions: dict) -> list[ReTrainSets]:
        """Read all re-train sets based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading all data from ReTrainSets database.",
        )

    def read_retrain_sets(self, filter_conditions: dict) -> list[ReTrainSets]:
        """Read re-train sets based on filter."""
        return self.read(
            filter_conditions,
            print_message="Error reading data from ReTrainSets database.",
        )

    def update_retrain_sets(self, update_lists: list[dict[str, dict]]) -> int:
        """Update re-train sets with provided data."""
        return self.update(
            update_lists, print_message="Error updating data in ReTrainSets database."
        )

    def delete_retrain_sets(self, filter_conditions: dict) -> int:
        """Delete re-train sets based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from ReTrainSets database.",
        )
