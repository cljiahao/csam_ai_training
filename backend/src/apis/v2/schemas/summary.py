from dataclasses import dataclass


@dataclass
class BaseSetsData:
    no_of_g: int = 0
    no_of_ng: int = 0
    no_of_others: int = 0


@dataclass
class EvalBaseKey:
    total_sum: int = 0


@dataclass
class EvalSetsData:
    colors_count: EvalBaseKey
    thousands_count: EvalBaseKey
    mass_pro_count: EvalBaseKey


@dataclass
class EvalBaseSets:
    id: int
    item: str
    eval_data: EvalSetsData
    base_data: BaseSetsData


@dataclass
class EvalBaseSetsData:
    augment_multiplier: int
    mass_pro_threshold: int
    colors_threshold: int
    thousands_threshold: int
    eval_base_sets: list[EvalBaseSets]
