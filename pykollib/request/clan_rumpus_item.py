from enum import Enum
from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from ..util import parsing
from .clan_rumpus import Furniture


class ItemFurniture(Enum):
    SodaMachine = Furniture.SodaMachine
    SnackMachine = Furniture.SnackMachine
    MrKlaw = Furniture.MrKlaw


def parse(html: str, **kwargs):
    return parsing.item(html)


def clan_rumpus_item(session: "pykollib.Session", furniture: ItemFurniture) -> Coroutine[Any, Any, ClientResponse]:
    "Uses the item dispensing machines in the clan rumpus room."
    spot, furni = furniture.value

    params = {"action": "click", "spot": spot, "furni": furni}
    return session.request("clan_rumpus.php", params=params, parse=parse)
