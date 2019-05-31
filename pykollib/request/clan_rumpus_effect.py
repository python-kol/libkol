from enum import Enum
from typing import Any, Dict, List

from .request import Request

import pykollib

from ..util import parsing


class Type(Enum):
    Jukebox = (3, 2)
    Radio = (4, 1)


class clan_rumpus_effect(Request):
    def __init__(self, session: "pykollib.Session", type: Type) -> None:
        """
        Uses an effect giver in the clan rumpus room.
        """

        super().__init__(session)

        params = {"action": "click", "spot": type.value[0], "furni": type.value[1]}
        self.request = session.request("clan_rumpus.php", params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> List[Dict[str, Any]]:
        return parsing.effects(html)
