from sqlalchemy.orm import Session

from db.models.eval_sets import EvalSets
from db.repository.base_repository import BaseRepository


class EvalSetsRepository(BaseRepository[EvalSets]):
    def __init__(self, db: Session):
        super().__init__(db, EvalSets)

    def create_eval_sets(self, eval_sets_data: dict) -> EvalSets:
        """Create new eval sets."""
        return self.create(
            eval_sets_data,
            print_message=f"Error creating eval sets from the database.",
        )

    def read_all_eval_sets(self, filter_conditions: dict) -> EvalSets:
        """Read all eval sets based on filter."""
        return self.read(
            filter_conditions,
            return_all=True,
            print_message=f"Error reading eval sets from the database.",
        )

    def read_eval_sets(self, filter_conditions: dict) -> EvalSets:
        """Read eval sets based on filter."""
        return self.read(
            filter_conditions,
            print_message=f"Error reading eval sets from the database.",
        )

    def update_eval_sets(self, updates_list: list[dict[str, dict]]) -> EvalSets:
        """Update eval sets with provided data."""
        return self.update(
            updates_list,
            print_message=f"Error updating eval sets in the database.",
        )

    def delete_eval_sets(self, filter_conditions: dict) -> EvalSets:
        """Delete eval sets based on filter."""
        return self.delete(
            filter_conditions,
            print_message=f"Error deleting eval sets from the database.",
        )
