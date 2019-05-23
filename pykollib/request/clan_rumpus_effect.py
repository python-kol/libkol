from enum import Enum
from aiohttp import ClientResponse
from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from ..Session import Session

from ..util import parsing


def parse(html: str, **kwargs) -> List[Dict[str, Any]]:
    return parsing.effects(html)


class Type(Enum):
    Jukebox = (3, 2)
    Radio = (4, 1)


def clan_rumpus_effect(session: "Session") -> ClientResponse:
    "Uses an effect giver in the clan rumpus room."

    params = {"action": "click", "spot": type.value[0], "furni": type.value[1]}
    return session.request("clan_rumpus.php", params=params, parse=parse)
