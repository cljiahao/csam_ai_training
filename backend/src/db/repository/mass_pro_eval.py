from sqlalchemy.orm import Session

from db.models.mass_pro_eval import MassProEval
from db.repository.base_repository import BaseRepository


class MassProEvalRepository(BaseRepository[MassProEval]):
    def __init__(self, db: Session):
        super().__init__(db, MassProEval)

    def create_mass_pro(self, mass_pro_data: dict) -> list[MassProEval]:
        """Create new mass pro eval sets."""
        return self.create(
            mass_pro_data,
            print_message="Error creating new data into MassProEval database.",
        )

    def read_mass_pro(self, filter_conditions: dict) -> list[MassProEval]:
        """Read mass pro eval sets based on filter."""
        return self.read(
            filter_conditions,
            print_message="Error reading data from MassProEval database.",
        )

    def update_mass_pro(self, update_lists: list[dict[str, dict]]) -> int:
        """Update mass pro eval sets with provided data."""
        return self.update(
            update_lists,
            print_message="Error updating data in MassProEval database.",
        )

    def delete_mass_pro(self, filter_conditions: dict) -> int:
        """Delete mass pro eval sets based on filter."""
        return self.delete(
            filter_conditions,
            print_message="Error deleting data from MassProEval database.",
        )
