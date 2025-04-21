from sqlalchemy.orm import Session

from db.models.thousands_eval import ThousandsEval
from db.repository.base_repository import BaseRepository


class ThousandsEvalRepository(BaseRepository[ThousandsEval]):
    def __init__(self, db: Session):
        super().__init__(db, ThousandsEval)

    def create_thousands(self, thousands_data: dict) -> list[ThousandsEval]:
        """Create new thousands eval sets."""
        return self.create(
            thousands_data,
            print_message="Error creating new data into ThousandsEval database.",
        )

    def read_thousands(self, filter_conditions: dict) -> list[ThousandsEval]:
        """Read thousands eval sets based on filter."""
        return self.read(
            filter_conditions,
            print_message="Error reading data from ThousandsEval database.",
        )

    def update_thousands(self, update_lists: list[dict[str, dict]]) -> int:
        """Update thousands eval sets with provided data."""
        return self.update(
            update_lists,
            print_message="Error updating data in ThousandsEval database.",
        )

    def delete_thousands(self, filter_conditions: dict) -> int:
        """Delete thousands eval sets based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from ThousandsEval database.",
        )
