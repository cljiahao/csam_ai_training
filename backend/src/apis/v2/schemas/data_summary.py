from pydantic import BaseModel


class BaseSetsData(BaseModel):
    no_of_g: int = 0
    no_of_ng: int = 0
    no_of_others: int = 0


class EvalBaseKey(BaseModel):
    total_sum: int = 0


class EvalSetsData(BaseModel):
    colors_count: EvalBaseKey
    thousands_count: EvalBaseKey
    mass_pro_count: EvalBaseKey


class EvalBaseSets(BaseModel):
    id: int
    item: str
    eval_data: EvalSetsData
    base_data: BaseSetsData


class EvalBaseSetsData(BaseModel):
    augment_multiplier: int
    mass_pro_threshold: int
    colors_threshold: int
    thousands_threshold: int
    eval_base_sets: list[EvalBaseSets]
