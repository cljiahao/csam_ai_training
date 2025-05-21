from sqlalchemy.orm import Session

from apis.v2.constants.csam_thresholds import AugmentThresholdRatio
from apis.v2.constants.datasets_thresholds import EvaluationDatasetsThresholds
from apis.v2.schemas.data_summary import (
    BaseSetsData,
    EvalBaseKey,
    TrainSetsSummary,
    ItemDataSets,
    DatasetsSummary,
    EvalSetsData,
    ReTrainSetsData,
)
from constants.colors import CSAMcolor
from constants.folder_names import ColorsFolderNames
from db.services.base_sets import BaseSetsService
from db.services.eval_sets import EvalSetsService
from db.services.retrain_sets import ReTrainSetsService
from utils.debug import timer


def get_datasets_summary(
    db: Session, is_train: bool
) -> TrainSetsSummary | DatasetsSummary:
    """Retrieves and returns a dataset (Train / Re-Train) summary."""
    if is_train:
        return get_eval_base_sets_data(db)
    else:
        return get_eval_retrain_sets_data(db)


@timer("Get Eval and Base Datasets")
def get_eval_base_sets_data(db: Session) -> TrainSetsSummary:
    """Retrieves and combines evaluation and base set data."""
    base_sets_data = get_all_base_sets_data(db)
    summary_kwargs = get_train_sets_list(base_sets_data, db)
    augment_multiplier = len(CSAMcolor) * AugmentThresholdRatio.BASE_MULTIPLIER
    return TrainSetsSummary(
        **summary_kwargs.model_dump(),
        augment_multiplier=augment_multiplier,
    )


@timer("Get Eval and Re-Train Datasets")
def get_eval_retrain_sets_data(db: Session) -> DatasetsSummary:
    """Retrieves and combines evaluation and reTrain set data."""
    retrain_sets_data = get_all_retrain_sets_data(db)
    return get_train_sets_list(retrain_sets_data, db)


def get_train_sets_list(
    train_sets_data: dict[str, BaseSetsData | ReTrainSetsData], db: Session
) -> DatasetsSummary:
    """Combines evaluation data with a provided training dataset."""
    eval_sets_data = get_all_eval_sets_data(db)

    train_sets_list = []
    all_keys: set[str] = set(eval_sets_data.keys()).union(train_sets_data.keys())
    for i, key in enumerate(all_keys):
        combined_entry = ItemDataSets(
            id=i + 1,
            item=key,
            eval_data=eval_sets_data.get(key, {}),
            train_data=train_sets_data.get(key, {}),
        )
        train_sets_list.append(combined_entry)

    colors_threshold = EvaluationDatasetsThresholds.PER_COLOR * len(ColorsFolderNames)

    thousands_small = EvaluationDatasetsThresholds.THOUSANDS_SMALL
    thousands_med_big = EvaluationDatasetsThresholds.THOUSANDS_MED_AND_BIG
    thousands_threshold = thousands_small + thousands_med_big * 2

    return DatasetsSummary(
        mass_pro_threshold=EvaluationDatasetsThresholds.MASS_PRO,
        colors_threshold=colors_threshold,
        thousands_threshold=thousands_threshold,
        train_sets_list=train_sets_list,
    )


def get_all_eval_sets_data(db: Session) -> dict[str, EvalSetsData]:
    """Fetches all evaluation set data and returns it as a dictionary keyed by item."""
    eval_sets_service = EvalSetsService(db)
    eval_sets_data_list = eval_sets_service.read_all_eval_sets()

    eval_sets_dict = {}
    for eval_set in eval_sets_data_list:
        total_colors_sum = sum_eval_attributes(eval_set.colors)
        total_thousands_sum = sum_eval_attributes(eval_set.thousands)
        total_mass_pro_plates = len(eval_set.mass_pro)

        eval_sets_dict[eval_set.item] = EvalSetsData(
            colors_count=EvalBaseKey(total_sum=total_colors_sum),
            thousands_count=EvalBaseKey(total_sum=total_thousands_sum),
            mass_pro_count=EvalBaseKey(total_sum=total_mass_pro_plates),
        )

    return eval_sets_dict


def get_all_base_sets_data(db: Session) -> dict[str, BaseSetsData]:
    """Fetches all base set data and returns it as a dictionary keyed by item."""
    base_sets_service = BaseSetsService(db)
    base_sets_data_list = base_sets_service.read_all_base_sets()

    return {
        base_set.item: BaseSetsData(
            no_of_g=base_set.no_of_g,
            no_of_ng=base_set.no_of_ng,
            no_of_others=base_set.no_of_others,
        )
        for base_set in base_sets_data_list
    }


def get_all_retrain_sets_data(db: Session) -> dict[str, ReTrainSetsData]:
    """Fetches all reTrain set data and returns it as a dictionary keyed by item."""
    retrain_sets_service = ReTrainSetsService(db)
    retrain_sets_data_list = retrain_sets_service.read_all_retrain_sets()

    return {
        retrain_sets.item: ReTrainSetsData(
            no_of_g=retrain_sets.no_of_g,
            no_of_ng=retrain_sets.no_of_ng,
        )
        for retrain_sets in retrain_sets_data_list
    }


def sum_eval_attributes(eval_objects, exclude_fields=None) -> int:
    """Utility function to sum all integer attributes of an eval object,
    excluding specified metadata fields.
    """
    if exclude_fields is None:
        exclude_fields = {"id", "date_created", "date_updated", "eval_sets_id"}

    return sum(
        sum(
            getattr(obj, col, 0)
            for col in obj.__table__.columns.keys()
            if col not in exclude_fields
        )
        for obj in eval_objects
    )
