from typing import List

from enum import Enum
from dataclasses import dataclass, field
from datetime import date, datetime

from dataclasses_json import dataclass_json, config
from marshmallow import fields

from .sample import Sample, legacy_sample_to_sample
from .hpo import HPOTerm


def legacy_hpo_to_symptom(legacy_hpo):
    hpo = HPOTerm.from_string(legacy_hpo["HPO"])
    return Symptom(
        active=legacy_hpo["Active"] == "1",
        date=datetime.fromisoformat(legacy_hpo["Date"]),
        hpo=hpo,
    )


def legacy_sample_to_patient(legacy_sample):
    sample = legacy_sample_to_sample(legacy_sample)
    return Patient(
        id=legacy_sample["Interal ID"],
        pedigree_id=legacy_sample["Pedigree"],
        sex=Sex(legacy_sample["Sex"] or "unknown"),
        affected=legacy_sample["Affected"] == "1",
        disease=legacy_sample["Disease"],
        symptoms=[],
        samples=[sample],
    )


class Sex(str, Enum):
    UNKNOWN = "unknown"
    FEMALE = "female"
    MALE = "male"


@dataclass_json
@dataclass
class Symptom:
    active: bool
    date: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso")
        )
    )
    hpo: HPOTerm = field(
        metadata=config(
            encoder=str,
            decoder=HPOTerm.from_string,
            mm_field=fields.String
        )
    )


@dataclass_json
@dataclass
class Patient:
    id: str
    pedigree_id: str
    sex: Sex
    affected: bool
    disease: str  # TODO: use constrained system (ICD, OMIM)
    symptoms: List[Symptom]
    samples: List[Sample]
