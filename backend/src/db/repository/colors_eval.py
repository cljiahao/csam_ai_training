from sqlalchemy.orm import Session

from db.models.colors_eval import ColorsEval
from db.repository.base_repository import BaseRepository


class ColorsEvalRepository(BaseRepository[ColorsEval]):
    def __init__(self, db: Session):
        super().__init__(db, ColorsEval)

    def create_color(self, color_data: dict) -> ColorsEval:
        """Create new color eval sets."""
        return self.create(
            color_data,
            print_message=f"Error creating color eval sets from the database.",
        )

    def read_color(self, filter_condition: dict) -> ColorsEval:
        """Read color eval sets based on filter."""
        return self.read(
            filter_condition,
            print_message=f"Error reading color eval sets from the database.",
        )

    def update_color(self, filter_condition: dict, update_data: dict) -> ColorsEval:
        """Update color eval sets with provided data."""
        return self.update(
            filter_condition,
            update_data,
            print_message=f"Error updating color eval sets in the database.",
        )

    def delete_color(self, filter_condition: dict) -> ColorsEval:
        """Delete color eval sets based on filter."""
        return self.delete(
            filter_condition,
            print_message=f"Error deleting color eval sets from the database.",
        )
