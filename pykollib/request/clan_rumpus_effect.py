from enum import Enum
from typing import Any, Coroutine, Dict, List

from aiohttp import ClientResponse

import pykollib

from ..util import parsing


def parse(html: str, **kwargs) -> List[Dict[str, Any]]:
    return parsing.effects(html)


class Type(Enum):
    Jukebox = (3, 2)
    Radio = (4, 1)


def clan_rumpus_effect(session: "pykollib.Session", type: Type) -> Coroutine[Any, Any, ClientResponse]:
    "Uses an effect giver in the clan rumpus room."

    params = {"action": "click", "spot": type.value[0], "furni": type.value[1]}
    return session.request("clan_rumpus.php", params=params, parse=parse)
