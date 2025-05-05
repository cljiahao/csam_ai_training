from sqlalchemy.orm import Session

from constants.folder_names import ColorsFolderNames, ThousandsFolderNames
from core.exceptions import InvalidInputError
from db.models.colors_eval import ColorsEval
from db.models.eval_sets import EvalSets
from db.models.mass_pro_eval import MassProEval
from db.models.thousands_eval import ThousandsEval
from db.repository.eval_sets import EvalSetsRepository
from db.repository.colors_eval import ColorsEvalRepository
from db.repository.mass_pro_eval import MassProEvalRepository
from db.repository.thousands_eval import ThousandsEvalRepository


class EvalSetsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.eval_sets_repo = EvalSetsRepository(db)
        self.colors_repo = ColorsEvalRepository(db)
        self.mass_pro_repo = MassProEvalRepository(db)
        self.thousands_repo = ThousandsEvalRepository(db)

    def read_all_eval_sets(self) -> list[EvalSets]:
        """Service layer method to read eval sets"""

        return self.eval_sets_repo.read_all_eval_sets({})

    def read_eval_sets(self, item: str) -> EvalSets:
        """Service layer method to read eval sets"""
        if not item:
            raise InvalidInputError("Item cannot be empty.")
        filter_conditions = {"item": item}

        return self.eval_sets_repo.read_eval_sets(filter_conditions)[0]

    def _read_or_create_eval_sets(self, item: str) -> EvalSets:
        """Read evaluation sets for an item, or create them if they don't exist."""
        eval_sets = self.read_eval_sets(item)
        if not eval_sets:
            eval_sets = self.eval_sets_repo.create_eval_sets({"item": item})[0]

        return eval_sets

    def _validate_eval_data_keys(
        self, data: dict, valid_keys: set, eval_type: str
    ) -> None:
        """Validate the keys in eval data."""
        invalid_keys = set(data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in {eval_type} data: {', '.join(invalid_keys)}"
            )

    def create_colors_eval(self, item: str, color_eval_data: dict) -> ColorsEval:
        """Service layer method to create new or update colors eval."""
        self._validate_eval_data_keys(
            color_eval_data, {item for item in ColorsFolderNames}, "Colors"
        )

        eval_sets = self._read_or_create_eval_sets(item)
        data_condition = {"eval_sets_id": eval_sets.id}

        if self.colors_repo.read_colors(data_condition)[0]:
            return self.colors_repo.update_colors(
                {"filter_conditions": data_condition, "update_data": color_eval_data}
            )

        color_eval_data.update(data_condition)
        return self.colors_repo.create_colors(color_eval_data)[0]

    def create_mass_pro_eval(
        self, item: str, plate_no: str, mass_pro_eval_data: dict
    ) -> MassProEval:
        """Service layer method to create new or update mass pro eval."""
        self._validate_eval_data_keys(
            mass_pro_eval_data, {"no_of_chips", "no_of_ng"}, "Mass Pro"
        )

        eval_sets = self._read_or_create_eval_sets(item)
        data_condition = {"eval_sets_id": eval_sets.id, "plate_no": plate_no}
        if self.mass_pro_repo.read_mass_pro(data_condition)[0]:
            return self.mass_pro_repo.update_mass_pro(
                {"filter_conditions": data_condition, "update_data": mass_pro_eval_data}
            )

        mass_pro_eval_data.update(data_condition)
        return self.mass_pro_repo.create_mass_pro(mass_pro_eval_data)[0]

    def create_thousands_eval(
        self, item: str, thousands_eval_data: dict
    ) -> ThousandsEval:
        """Service layer method to create new or update thousands eval."""
        self._validate_eval_data_keys(
            thousands_eval_data, {item for item in ThousandsFolderNames}, "Thousands"
        )

        eval_sets = self._read_or_create_eval_sets(item)
        data_condition = {"eval_sets_id": eval_sets.id}

        if self.thousands_repo.read_thousands(data_condition)[0]:
            return self.thousands_repo.update_thousands(
                {
                    "filter_conditions": data_condition,
                    "update_data": thousands_eval_data,
                }
            )

        thousands_eval_data.update(data_condition)
        return self.thousands_repo.create_thousands(thousands_eval_data)[0]
