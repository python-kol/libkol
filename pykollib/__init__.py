import asyncio
from typing import Callable

from .Clan import Clan
from .Error import Error
from .FoldGroup import FoldGroup
from .Item import Item
from . import types
from .Kmail import Kmail
from .Session import Session, models
from .ZapGroup import ZapGroup
from .Store import Store
from .Trophy import Trophy
from .Effect import Effect
from .Modifier import Modifier


def run(func: Callable):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())
    loop.close()


__all__ = [
    "Clan",
    "Error",
    "Session",
    "Kmail",
    "Item",
    "types",
    "FoldGroup",
    "ZapGroup",
    "Store",
    "Trophy",
    "Effect",
    "Modifier",
    "models",
]
