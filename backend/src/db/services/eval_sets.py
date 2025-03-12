from sqlalchemy.orm import Session

from constants.image_thresholds import EvalColorNames, EvalThousandNames
from core.exceptions import InvalidInputError
from db.models.colors_eval import ColorsEval
from db.models.eval_sets import EvalSets
from db.models.mass_pro_eval import MassProEval
from db.models.thousand_eval import ThousandEval
from db.repository.eval_sets import EvalSetsRepository
from db.repository.colors_eval import ColorsEvalRepository
from db.repository.mass_pro_eval import MassProEvalRepository
from db.repository.thousand_eval import ThousandEvalRepository


class EvalSetsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.eval_sets_repo = EvalSetsRepository(db)
        self.colors_repo = ColorsEvalRepository(db)
        self.mass_pro_repo = MassProEvalRepository(db)
        self.thousand_repo = ThousandEvalRepository(db)

    def read_eval_sets(self, item: str) -> EvalSets:
        """Service layer method to read eval sets"""
        if not item:
            raise InvalidInputError("Item cannot be empty.")
        filter_condition = {"item": item}

        return self.eval_sets_repo.read_eval_sets(filter_condition)

    def _read_or_create_eval_sets(self, item: str) -> EvalSets:
        eval_sets = self.read_eval_sets(item)
        if not eval_sets:
            eval_sets = self.eval_sets_repo.create_eval_sets({"item": item})

        return eval_sets

    def _validate_eval_data_keys(
        self, data: dict, valid_keys: set, eval_type: str
    ) -> None:
        """Validate the keys in eval data."""
        invalid_keys = set(data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(f"Unknown {eval_type} keys: {invalid_keys}")

    def create_color_eval(self, item: str, color_eval_data: dict) -> ColorsEval:
        """Service layer method to create new or update color eval."""
        self._validate_eval_data_keys(
            color_eval_data, {e.value for e in EvalColorNames}, "Color"
        )

        eval_sets = self._read_or_create_eval_sets(item)
        data_condition = {"eval_sets_id": eval_sets.id}

        if self.colors_repo.read_color(data_condition):
            return self.colors_repo.update_color(data_condition, color_eval_data)

        color_eval_data.update({"eval_sets_id": eval_sets.id})
        return self.colors_repo.create_color(color_eval_data)

    def create_mass_pro_eval(self, item: str, mass_pro_eval_data: dict) -> MassProEval:
        """Service layer method to create new or update mass pro eval."""
        self._validate_eval_data_keys(
            mass_pro_eval_data, {"plate_no", "no_of_chips"}, "Mass Pro"
        )

        eval_sets = self._read_or_create_eval_sets(item)
        data_condition = {"eval_sets_id": eval_sets.id}

        if self.mass_pro_repo.read_mass_pro(data_condition):
            return self.mass_pro_repo.update_mass_pro(
                data_condition, mass_pro_eval_data
            )

        mass_pro_eval_data.update({"eval_sets_id": eval_sets.id})
        return self.mass_pro_repo.create_mass_pro(mass_pro_eval_data)

    def create_thousand_eval(self, item: str, thousand_eval_data: dict) -> ThousandEval:
        """Service layer method to create new or update thousand eval."""
        self._validate_eval_data_keys(
            thousand_eval_data, {e.value for e in EvalThousandNames}, "Thousand"
        )

        eval_sets = self._read_or_create_eval_sets(item)
        data_condition = {"eval_sets_id": eval_sets.id}

        if self.thousand_repo.read_thousand(data_condition):
            return self.thousand_repo.update_thousand(
                data_condition, thousand_eval_data
            )

        thousand_eval_data.update({"eval_sets_id": eval_sets.id})
        return self.thousand_repo.create_thousand(thousand_eval_data)
