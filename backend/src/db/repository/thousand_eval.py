from sqlalchemy.orm import Session

from db.models.thousand_eval import ThousandEval
from db.repository.base_repository import BaseRepository


class ThousandEvalRepository(BaseRepository[ThousandEval]):
    def __init__(self, db: Session):
        super().__init__(db, ThousandEval)

    def create_thousand(self, thousand_data: dict) -> ThousandEval:
        """Create new thousand eval sets."""
        return self.create(
            thousand_data,
            print_message=f"Error creating thousand eval sets from the database.",
        )

    def read_thousand(self, filter_condition: dict) -> ThousandEval:
        """Read thousand eval sets based on filter."""
        return self.read(
            filter_condition,
            print_message=f"Error reading thousand eval sets from the database.",
        )

    def update_thousand(
        self, filter_condition: dict, update_data: dict
    ) -> ThousandEval:
        """Update thousand eval sets with provided data."""
        return self.update(
            filter_condition,
            update_data,
            print_message=f"Error updating thousand eval sets in the database.",
        )

    def delete_thousand(self, filter_condition: dict) -> ThousandEval:
        """Delete thousand eval sets based on filter."""
        return self.delete(
            filter_condition,
            print_message=f"Error deleting thousand eval sets from the database.",
        )
