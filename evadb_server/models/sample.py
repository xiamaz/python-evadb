"""
Streamlined representation for samples, parsed from the perl base.
"""
from enum import Enum
from dataclasses import dataclass, field
import datetime

from dataclasses_json import dataclass_json, config
from marshmallow import fields


def legacy_sample_to_sample(legacy_sample):
    status_key = [k for k in legacy_sample if "Con- clusion" in k][0]
    status_value = legacy_sample[status_key]

    if status_value.startswith("0"):
        status = SampleStatus.NONE
    elif status_value.startswith("1"):
        status = SampleStatus.SOLVED
    elif status_value.startswith("2"):
        status = SampleStatus.UNSOLVED
    elif status_value.startswith("3"):
        status = SampleStatus.CANDIDATE
    elif status_value.startswith("4"):
        status = SampleStatus.PENDING
    else:
        status = SampleStatus.UNKNOWN

    tissue_value = legacy_sample["Tissue"]
    if tissue_value == "peripheral blood":
        tissue = TissueType.BLOOD
    else:
        tissue = TissueType.UNKNOWN

    return Sample(
        id=legacy_sample["Interal ID"],
        foreign_id=legacy_sample["Foreign ID"],
        external_seq_id=legacy_sample["External SeqID"],
        patient_id=legacy_sample["Interal ID"],
        status=status,
        tissue=tissue,
        comment=legacy_sample["Comment"],
        cooperation=legacy_sample["Cooperation"],
        date=datetime.date.fromisoformat(legacy_sample["Entered"]),
    )


class SampleStatus(str, Enum):
    UNKNOWN = "unknown"
    NONE = "none"
    SOLVED = "solved"
    UNSOLVED = "unsolved"
    CANDIDATE = "candidate"
    PENDING = "pending"


class TissueType(str, Enum):
    UNKNOWN = "unknown"
    BLOOD = "blood"


@dataclass_json
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
    date: datetime.date = field(
        metadata=config(
            encoder=datetime.date.isoformat,
            decoder=datetime.date.fromisoformat,
            mm_field=fields.DateTime(format="iso")
        )
    )
