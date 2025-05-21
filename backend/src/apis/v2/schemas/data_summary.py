from pydantic import BaseModel


class CSAMSetsData(BaseModel):
    no_of_g: int = 0
    no_of_ng: int = 0


class BaseSetsData(CSAMSetsData):
    no_of_others: int = 0


class ReTrainSetsData(CSAMSetsData):
    pass


class EvalBaseKey(BaseModel):
    total_sum: int = 0


class EvalSetsData(BaseModel):
    colors_count: EvalBaseKey
    thousands_count: EvalBaseKey
    mass_pro_count: EvalBaseKey


class ItemDataSets(BaseModel):
    id: int
    item: str
    eval_data: EvalSetsData
    train_data: BaseSetsData | ReTrainSetsData


class EvalSummary(BaseModel):
    mass_pro_threshold: int
    colors_threshold: int
    thousands_threshold: int


class DatasetsSummary(EvalSummary):
    train_sets_list: list[ItemDataSets]


class TrainSetsSummary(DatasetsSummary):
    augment_multiplier: int
