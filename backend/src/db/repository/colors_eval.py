from sqlalchemy.orm import Session

from db.models.colors_eval import ColorsEval
from db.repository.base_repository import BaseRepository


class ColorsEvalRepository(BaseRepository[ColorsEval]):
    def __init__(self, db: Session):
        super().__init__(db, ColorsEval)

    def create_colors(self, colors_data: dict) -> list[ColorsEval]:
        """Create new colors eval sets."""
        return self.create(
            colors_data,
            print_message="Error creating new data into ColorsEval database.",
        )

    def read_colors(self, filter_conditions: dict) -> list[ColorsEval]:
        """Read colors eval sets based on filter."""
        return self.read(
            filter_conditions,
            print_message="Error reading data from ColorsEval database.",
        )

    def update_colors(self, update_lists: dict[str, dict]) -> int:
        """Update colors eval sets with provided data."""
        return self.update(
            update_lists,
            print_message="Error updating data in ColorsEval database.",
        )

    def delete_colors(self, filter_conditions: dict) -> int:
        """Delete colors eval sets based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from ColorsEval database.",
        )
