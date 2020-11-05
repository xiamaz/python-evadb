import re
from dataclasses import dataclass


HPO_REGEX = re.compile(r"^HP:(\d{7})$")


class HPOTerm:
    """Represent a single HPO term."""

    def __init__(self, hpo_id):
        self._id = hpo_id

    @property
    def id(self):
        return self._id

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
        return hpo_str

    def __eq__(self, other):
        return str(self) == str(other)
