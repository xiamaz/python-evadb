from typing import List

from enum import Enum, auto
from dataclasses import dataclass
from datetime import date

from .sample import Sample
from .hpo import HPOTerm


class Sex(Enum):
    UNKNOWN = auto
    FEMALE = auto
    MALE = auto


@dataclass
class Symptom:
    active: bool
    date: date
    hpo: HPOTerm


@dataclass
class Patient:
    id: str
    pedigree_id: str
    sex: Sex
    affected: bool
    disease: str  # TODO: use constrained system (ICD, OMIM)
    symptoms: List[Symptom]
