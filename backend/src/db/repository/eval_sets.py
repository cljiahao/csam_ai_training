from sqlalchemy.orm import Session

from db.models.eval_sets import EvalSets
from db.repository.base_repository import BaseRepository


class EvalSetsRepository(BaseRepository[EvalSets]):
    def __init__(self, db: Session):
        super().__init__(db, EvalSets)

    def create_eval_sets(self, eval_sets_data: dict) -> list[EvalSets]:
        """Create new eval sets."""
        return self.create(
            eval_sets_data,
            print_message="Error creating new data into EvalSets database.",
        )

    def read_all_eval_sets(self, filter_conditions: dict) -> list[EvalSets]:
        """Read all eval sets based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message="Error reading all data from EvalSets database.",
        )

    def read_eval_sets(self, filter_conditions: dict) -> list[EvalSets]:
        """Read eval sets based on filter."""
        return self.read(
            filter_conditions,
            print_message="Error reading data from EvalSets database.",
        )

    def update_eval_sets(self, update_lists: list[dict[str, dict]]) -> int:
        """Update eval sets with provided data."""
        return self.update(
            update_lists,
            print_message="Error updating data in EvalSets database.",
        )

    def delete_eval_sets(self, filter_conditions: dict) -> int:
        """Delete eval sets based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from EvalSets database.",
        )
