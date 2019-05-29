from enum import Enum
from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..util import parsing
from .clan_rumpus import Furniture


class MeatFurniture(Enum):
    Orchid = Furniture.MeatOrchid
    Tree = Furniture.MeatTree
    Bush = Furniture.MeatBush


def parse(html: str) -> int:
    return parsing.meat(html)


def clan_rumpus_meat(session: "Session", furniture: MeatFurniture) -> ClientResponse:
    "Uses the meat bush in the clan rumpus room."
    spot, furni = furniture.value

    params = {"action": "click", "spot": spot, "furni": furni}
    return session.request("clan_rumpus.php", params=params, parse=parse)