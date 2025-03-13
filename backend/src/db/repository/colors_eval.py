from sqlalchemy.orm import Session

from db.models.colors_eval import ColorsEval
from db.repository.base_repository import BaseRepository


class ColorsEvalRepository(BaseRepository[ColorsEval]):
    def __init__(self, db: Session):
        super().__init__(db, ColorsEval)

    def create_colors(self, colors_data: dict) -> ColorsEval:
        """Create new colors eval sets."""
        return self.create(
            colors_data,
            print_message=f"Error creating colors eval sets from the database.",
        )

    def read_colors(self, filter_condition: dict) -> ColorsEval:
        """Read colors eval sets based on filter."""
        return self.read(
            filter_condition,
            print_message=f"Error reading colors eval sets from the database.",
        )

    def update_colors(self, filter_condition: dict, update_data: dict) -> ColorsEval:
        """Update colors eval sets with provided data."""
        return self.update(
            filter_condition,
            update_data,
            print_message=f"Error updating colors eval sets in the database.",
        )

    def delete_colors(self, filter_condition: dict) -> ColorsEval:
        """Delete colors eval sets based on filter."""
        return self.delete(
            filter_condition,
            print_message=f"Error deleting colors eval sets from the database.",
        )
