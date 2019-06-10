from enum import Enum
from typing import Any, Dict, List

import libkol

from ..util import parsing
from .request import Request


class Type(Enum):
    Jukebox = (3, 2)
    Radio = (4, 1)


class clan_rumpus_effect(Request[List[Dict[str, Any]]]):
    """
    Uses an effect giver in the clan rumpus room.
    """

    def __init__(self, session: "libkol.Session", type: Type) -> None:
        super().__init__(session)

        params = {"action": "click", "spot": type.value[0], "furni": type.value[1]}
        self.request = session.request("clan_rumpus.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Dict[str, Any]]:
        return parsing.effects(content)
