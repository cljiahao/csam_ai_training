from sqlalchemy.orm import Session

from constants.folder_names import ReTrainFolderName
from core.exceptions import InvalidInputError
from db.models.retrain_sets import ReTrainSets
from db.repository.retrain_sets import ReTrainSetsRepository


class ReTrainSetsService:
    def __init__(self, db: Session):
        """Initialize service with repository."""
        self.repo = ReTrainSetsRepository(db)

    def _validate_retrain_sets_keys(self, retrain_sets_data: dict) -> None:
        """Validate the keys in the re-train sets data."""
        invalid_keys = set(retrain_sets_data) - set(ReTrainFolderName)
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in re-train sets data: {', '.join(invalid_keys)}"
            )

    def read_all_retrain_sets(self) -> list[ReTrainSets]:
        """Service layer method to read re-train sets"""

        return self.repo.read_all_retrain_sets({})

    def read_retrain_sets(self, item: str) -> ReTrainSets:
        """Service layer method to read re-train sets"""
        if not item:
            raise InvalidInputError("Filter conditions: Item cannot be empty.")
        filter_conditions = {"item": item}

        return self.repo.read_retrain_sets(filter_conditions)[0]

    def create_or_update_retrain_sets(
        self, item: str, retrain_sets_data: dict[str, int]
    ) -> ReTrainSets | int:
        """Service layer method to create new or update re-train sets"""
        if not item:
            raise InvalidInputError("Filter conditions: Item cannot be empty.")

        self._validate_retrain_sets_keys(retrain_sets_data)

        data_condition = {"item": item}
        new_retrain_sets_data = {
            f"no_of_{k.lower()}": v for k, v in retrain_sets_data.items()
        }

        existing_retrain_sets = self.read_retrain_sets(item)
        if existing_retrain_sets:
            self.repo.update_retrain_sets(
                {
                    "filter_conditions": data_condition,
                    "update_data": new_retrain_sets_data,
                }
            )
            return self.read_retrain_sets(item)

        new_retrain_sets_data.update(data_condition)
        return self.repo.create_retrain_sets(new_retrain_sets_data)[0]
