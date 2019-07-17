from enum import Enum
from typing import List

from .CharacterClass import CharacterClass


class Stat(Enum):
    Muscle = "muscle"
    Mysticality = "mysticality"
    Moxie = "moxie"

    def __contains__(self, character_class: CharacterClass) -> bool:
        return character_class.stat == self

    @property
    def substats(self) -> List[str]:
        if self is self.Muscle:
            return [
                "Beefiness",
                "Fortitude",
                "Muscleboundness",
                "Strengthliness",
                "Strongness",
            ]
        if self is self.Mysticality:
            return ["Enchantedness", "Magicalness", "Mysteriousness", "Wizardliness"]
        if self is self.Moxie:
            return ["Cheek", "Chutzpah", "Roguishness", "Sarcasm", "Smarm"]

        return []
