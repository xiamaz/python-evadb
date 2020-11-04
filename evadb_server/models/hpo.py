import re
from dataclasses import dataclass


HPO_REGEX = re.compile(r"^HP:(\d{7})$")


@dataclass
class HPOTerm(frozen=True, eq=True):
    """Represent a single HPO term."""
    id: int

    @classmethod
    def from_string(cls, string):
        match = HPO_REGEX.match(string)
        if not match:
            raise ValueError(f"Cannot convert {string} to HPO Term")

        hpo_id = int(match[1])
        return cls(hpo_id)

    def __repr__(self):
        """Pad the HPO String to a 7 string number."""
        hpo_str = f"HP:{self.id:07}"
