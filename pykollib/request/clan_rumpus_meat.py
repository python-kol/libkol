from enum import Enum
from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from ..util import parsing
from .clan_rumpus import Furniture


class MeatFurniture(Enum):
    Orchid = Furniture.MeatOrchid
    Tree = Furniture.MeatTree
    Bush = Furniture.MeatBush


def parse(html: str) -> int:
    return parsing.meat(html)


def clan_rumpus_meat(session: "pykollib.Session", furniture: MeatFurniture) -> Coroutine[Any, Any, ClientResponse]:
    "Uses the meat bush in the clan rumpus room."
    spot, furni = furniture.value

    params = {"action": "click", "spot": spot, "furni": furni}
    return session.request("clan_rumpus.php", params=params, parse=parse)
