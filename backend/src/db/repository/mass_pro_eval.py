from sqlalchemy.orm import Session

from db.models.mass_pro_eval import MassProEval
from db.repository.base_repository import BaseRepository


class MassProEvalRepository(BaseRepository[MassProEval]):
    def __init__(self, db: Session):
        super().__init__(db, MassProEval)

    def create_mass_pro(self, mass_pro_data: dict) -> MassProEval:
        """Create new mass pro eval sets."""
        return self.create(
            mass_pro_data,
            print_message=f"Error creating mass pro eval sets from the database.",
        )

    def read_mass_pro(self, filter_conditions: dict) -> MassProEval:
        """Read mass pro eval sets based on filter."""
        return self.read(
            filter_conditions,
            print_message=f"Error reading mass pro eval sets from the database.",
        )

    def update_mass_pro(self, updates_list: list[dict[str, dict]]) -> MassProEval:
        """Update mass pro eval sets with provided data."""
        return self.update(
            updates_list,
            print_message=f"Error updating mass pro eval sets in the database.",
        )

    def delete_mass_pro(self, filter_conditions: dict) -> MassProEval:
        """Delete mass pro eval sets based on filter."""
        return self.delete(
            filter_conditions,
            print_message=f"Error deleting mass pro eval sets from the database.",
        )
