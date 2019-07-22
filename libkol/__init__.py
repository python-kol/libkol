import asyncio
from typing import Callable

from . import types
from .Bonus import Bonus
from .CharacterClass import CharacterClass
from .Clan import Clan
from .Element import Element
from .Effect import Effect
from .Error import Error
from .Familiar import Familiar
from .FoldGroup import FoldGroup
from .Item import Item
from .Kmail import Kmail
from .Maximizer import Maximizer
from .Modifier import Modifier
from .Monster import Monster
from .MonsterDrop import MonsterDrop
from .MonsterImage import MonsterImage
from .Outfit import Outfit
from .OutfitVariant import OutfitVariant
from .Phylum import Phylum
from .Session import Session, models
from .Skill import Skill
from .Store import Store
from .Stat import Stat
from .Slot import Slot
from .Trophy import Trophy
from .ZapGroup import ZapGroup


def run(func: Callable):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())
    loop.close()


__all__ = [
    "Bonus",
    "CharacterClass",
    "Clan",
    "Element",
    "Effect",
    "Error",
    "Familiar",
    "FoldGroup",
    "Item",
    "Kmail",
    "Maximizer",
    "Monster",
    "MonsterDrop",
    "MonsterImage",
    "models",
    "Modifier",
    "Outfit",
    "OutfitVariant",
    "Phylum",
    "Session",
    "Skill",
    "Store",
    "Stat",
    "Slot",
    "Trophy",
    "types",
    "ZapGroup",
]
