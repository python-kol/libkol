from enum import Enum
from typing import List

from .request import Request

import pykollib

from ..util import parsing
from ..Item import ItemQuantity
from .clan_rumpus import Furniture


class ItemFurniture(Enum):
    SodaMachine = Furniture.SodaMachine
    SnackMachine = Furniture.SnackMachine
    MrKlaw = Furniture.MrKlaw


class clan_rumpus_item(Request):
    def __init__(self, session: "pykollib.Session", furniture: ItemFurniture) -> None:
        """
        Uses the item dispensing machines in the clan rumpus room.
        """
        super().__init__(session)
        spot, furni = furniture.value

        params = {"action": "click", "spot": spot, "furni": furni}
        self.request = session.request("clan_rumpus.php", params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> List[ItemQuantity]:
        return parsing.item(html)
