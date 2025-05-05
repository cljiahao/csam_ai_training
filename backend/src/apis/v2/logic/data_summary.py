from sqlalchemy.orm import Session

from apis.v2.constants.csam_thresholds import AugmentThresholdRatio
from apis.v2.constants.datasets_thresholds import EvaluationDatasetsThresholds
from apis.v2.schemas.data_summary import (
    BaseSetsData,
    EvalBaseKey,
    EvalBaseSets,
    EvalBaseSetsData,
    EvalSetsData,
)
from constants.colors import CSAMcolor
from constants.folder_names import ColorsFolderNames
from core.logging import logger
from db.services.base_sets import BaseSetsService
from db.services.eval_sets import EvalSetsService
from utils.debug import timer


@timer("Get Eval and Base Datasets")
def get_eval_base_sets_data(db: Session) -> EvalBaseSetsData:
    """Retrieves and combines evaluation and base set data."""
    augment_multiplier = len(CSAMcolor) * AugmentThresholdRatio.BASE_MULTIPLIER

    eval_set_data = get_all_eval_sets_data(db)
    base_set_data = get_all_base_sets_data(db)

    eval_base_set_data = []
    for i, key in enumerate(set(eval_set_data.keys()).union(base_set_data.keys())):
        combined_entry = EvalBaseSets(
            id=i + 1,
            item=key,
            eval_data=eval_set_data.get(key, {}),
            base_data=base_set_data.get(key, BaseSetsData()),
        )
        eval_base_set_data.append(combined_entry)

    thousands_small = EvaluationDatasetsThresholds.THOUSANDS_SMALL
    thousands_med_big = EvaluationDatasetsThresholds.THOUSANDS_MED_AND_BIG
    return EvalBaseSetsData(
        augment_multiplier=augment_multiplier,
        mass_pro_threshold=EvaluationDatasetsThresholds.MASS_PRO,
        colors_threshold=EvaluationDatasetsThresholds.PER_COLOR
        * len(ColorsFolderNames),
        thousands_threshold=thousands_small + thousands_med_big * 2,
        eval_base_sets=eval_base_set_data,
    )


def get_all_eval_sets_data(db: Session) -> dict:
    """Fetches all evaluation set data and returns it as a dictionary keyed by item."""
    eval_sets_service = EvalSetsService(db)
    eval_sets_data_list = eval_sets_service.read_all_eval_sets()

    eval_sets_dict = {}
    for eval_set in eval_sets_data_list:
        total_colors_sum = _sum_eval_attributes(eval_set.colors)
        total_thousands_sum = _sum_eval_attributes(eval_set.thousands)
        total_mass_pro_plates = len(eval_set.mass_pro)

        logger.info(
            f"Item {eval_set.item}: Colors={total_colors_sum}, Thousands={total_thousands_sum}, MassPro={total_mass_pro_plates}"
        )

        eval_sets_dict[eval_set.item] = EvalSetsData(
            colors_count=EvalBaseKey(total_sum=total_colors_sum),
            thousands_count=EvalBaseKey(total_sum=total_thousands_sum),
            mass_pro_count=EvalBaseKey(total_sum=total_mass_pro_plates),
        )

    return eval_sets_dict


def get_all_base_sets_data(db: Session) -> dict:
    """Fetches all base set data and returns it as a dictionary keyed by item."""
    base_sets_service = BaseSetsService(db)
    base_sets_data_list = base_sets_service.read_all_base_sets()

    base_sets_dict = {
        base_set.item: BaseSetsData(
            no_of_g=base_set.no_of_g,
            no_of_others=base_set.no_of_others,
            no_of_ng=base_set.no_of_ng,
        )
        for base_set in base_sets_data_list
    }

    return base_sets_dict


def _sum_eval_attributes(eval_objects, exclude_fields=None) -> int:
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
