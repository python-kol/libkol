from enum import Enum

from .Modifier import Modifier
from .Error import UnknownError


class Element(Enum):
    Cold = "cold"
    Hot = "hot"
    Sleaze = "sleeze"
    Spooky = "spooky"
    Stench = "stench"

    @property
    def damage(self) -> Modifier:
        modifier = (
            Modifier.ColdDamage
            if self is Element.Cold
            else Modifier.HotDamage
            if self is Element.Hot
            else Modifier.SleazeDamage
            if self is Element.Sleaze
            else Modifier.SpookyDamage
            if self is Element.Spooky
            else Modifier.StenchDamage
            if self is Element.Stench
            else None
        )

        if modifier is None:
            raise UnknownError(f"No matching damage to {self}")

        return modifier

    @property
    def resistance(self) -> Modifier:
        modifier = (
            Modifier.ColdResistance
            if self is Element.Cold
            else Modifier.HotResistance
            if self is Element.Hot
            else Modifier.SleazeResistance
            if self is Element.Sleaze
            else Modifier.SpookyResistance
            if self is Element.Spooky
            else Modifier.StenchResistance
            if self is Element.Stench
            else None
        )

        if modifier is None:
            raise UnknownError(f"No matching resistance to {self}")

        return modifier

    @property
    def immunity(self) -> Modifier:
        modifier = (
            Modifier.ColdImmunity
            if self is Element.Cold
            else Modifier.HotImmunity
            if self is Element.Hot
            else Modifier.SleazeImmunity
            if self is Element.Sleaze
            else Modifier.SpookyImmunity
            if self is Element.Spooky
            else Modifier.StenchImmunity
            if self is Element.Stench
            else None
        )

        if modifier is None:
            raise UnknownError(f"No matching immunity to {self}")

        return modifier
