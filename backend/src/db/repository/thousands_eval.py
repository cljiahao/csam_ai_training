from sqlalchemy.orm import Session

from db.models.thousands_eval import ThousandsEval
from db.repository.base_repository import BaseRepository


class ThousandsEvalRepository(BaseRepository[ThousandsEval]):
    def __init__(self, db: Session):
        super().__init__(db, ThousandsEval)

    def create_thousands(self, thousands_data: dict) -> ThousandsEval:
        """Create new thousands eval sets."""
        return self.create(
            thousands_data,
            print_message=f"Error creating thousands eval sets from the database.",
        )

    def read_thousands(self, filter_conditions: dict) -> ThousandsEval:
        """Read thousands eval sets based on filter."""
        return self.read(
            filter_conditions,
            print_message=f"Error reading thousands eval sets from the database.",
        )

    def update_thousands(self, updates_list: list[dict[str, dict]]) -> ThousandsEval:
        """Update thousands eval sets with provided data."""
        return self.update(
            updates_list,
            print_message=f"Error updating thousands eval sets in the database.",
        )

    def delete_thousands(self, filter_conditions: dict) -> ThousandsEval:
        """Delete thousands eval sets based on filter."""
        return self.delete(
            filter_conditions,
            print_message=f"Error deleting thousands eval sets from the database.",
        )
