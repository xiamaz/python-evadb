"""
Streamlined representation for samples, parsed from the perl base.
"""
from enum import Enum, auto
from dataclasses import dataclass
from datetime import date


class SampleStatus(Enum):
    NONE = auto
    SOLVED = auto
    UNSOLVED = auto
    CANDIDATE = auto
    PENDING = auto


class TissueType(Enum):
    UNKNOWN = auto
    BLOOD = auto


@dataclass
class Sample:
    id: str
    foreign_id: str
    external_seq_id: str
    patient_id: str
    status: SampleStatus
    tissue: TissueType
    comment: str
    cooperation: str
    date: date
