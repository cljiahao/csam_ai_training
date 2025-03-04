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

    def _read_eval_sets(self, item: str) -> EvalSets:
        """Service layer method to read eval sets"""
        filter_condition = {"item": item}

        return self.eval_sets_repo.read_eval_sets(filter_condition)

    def _read_or_create_eval_sets(self, item: str) -> EvalSets:
        if not item:
            raise InvalidInputError()
        eval_sets = self._read_eval_sets(item)
        if not eval_sets:
            eval_sets = self.eval_sets_repo.create_eval_sets({"item": item})

        return eval_sets

    def create_color_eval(self, item: str, color_eval_data: dict) -> ColorsEval:
        """Service layer method to create new or update color eval"""
        if set(color_eval_data) - set([e.value for e in EvalColorNames]):
            raise InvalidInputError(
                f"Unknown Color keys: {set([e.value for e in EvalColorNames]) - set(color_eval_data)}"
            )

        eval_sets = self._read_or_create_eval_sets(item)
        data_condition = {"eval_sets_id": eval_sets.id}

        if self.colors_repo.read_color(data_condition):
            return self.colors_repo.update_color(data_condition, color_eval_data)

        color_eval_data.update({"eval_sets_id": eval_sets.id})

        return self.colors_repo.create_color(color_eval_data)

    def create_mass_pro_eval(self, item: str, mass_pro_eval_data: dict) -> MassProEval:
        """Service layer method to create new or update mass pro eval"""
        if not any(key in mass_pro_eval_data for key in ["plate_no", "no_of_chips"]):
            raise InvalidInputError(
                f"Unknown Mass Pro keys: {set(['plate_no', 'no_of_chips']) - set(mass_pro_eval_data)}"
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
        """Service layer method to create new or update thousand eval"""
        if set(thousand_eval_data) - set([e.value for e in EvalThousandNames]):
            raise InvalidInputError(
                f"Unknown Thousand keys: {set([e.value for e in EvalThousandNames]) - set(thousand_eval_data)}"
            )

        eval_sets = self._read_or_create_eval_sets(item)
        data_condition = {"eval_sets_id": eval_sets.id}

        if self.thousand_repo.read_thousand(data_condition):
            return self.thousand_repo.update_thousand(
                data_condition, thousand_eval_data
            )

        thousand_eval_data.update({"eval_sets_id": eval_sets.id})

        return self.thousand_repo.create_thousand(thousand_eval_data)
