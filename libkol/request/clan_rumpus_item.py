from enum import Enum
from typing import List

import libkol

from libkol import types
from ..util import parsing
from .clan_rumpus import Furniture
from .request import Request

ItemQuantity = types.ItemQuantity


class ItemFurniture(Enum):
    SodaMachine = Furniture.SodaMachine
    SnackMachine = Furniture.SnackMachine
    MrKlaw = Furniture.MrKlaw


class clan_rumpus_item(Request[List[ItemQuantity]]):
    """
    Uses an item dispenser in the clan rumpus room.
    """

    def __init__(self, session: "libkol.Session", furniture: ItemFurniture) -> None:
        super().__init__(session)
        spot, furni = furniture.value

        params = {"action": "click", "spot": spot, "furni": furni}
        self.request = session.request("clan_rumpus.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[ItemQuantity]:
        return await parsing.item(content)
