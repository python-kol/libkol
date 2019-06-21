import asyncio
from typing import Callable

from . import types
from .Bonus import Bonus
from .CharacterClass import CharacterClass
from .Clan import Clan
from .Effect import Effect
from .Error import Error
from .FoldGroup import FoldGroup
from .Item import Item
from .Kmail import Kmail
from .Maximizer import Maximizer
from .Modifier import Modifier
from .Outfit import Outfit
from .Session import Session, models
from .Skill import Skill
from .Store import Store
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
    "Effect",
    "Error",
    "FoldGroup",
    "Item",
    "Kmail",
    "Maximizer",
    "models",
    "Modifier",
    "Outfit",
    "Session",
    "Skill",
    "Store",
    "Trophy",
    "types",
    "ZapGroup",
]
