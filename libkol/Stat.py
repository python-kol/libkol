from enum import Enum

from .CharacterClass import CharacterClass

class Stat(Enum):
    Muscle = "muscle"
    Mysticality = "mysticality"
    Moxie = "moxie"

    def __contains__(self, character_class: CharacterClass) -> bool:
        return character_class.stat == self
