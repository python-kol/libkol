from enum import Enum


from .request import Request

import pykollib

from ..util import parsing
from .clan_rumpus import Furniture


class MeatFurniture(Enum):
    Orchid = Furniture.MeatOrchid
    Tree = Furniture.MeatTree
    Bush = Furniture.MeatBush


class clan_rumpus_meat(Request):
    def __init__(self, session: "pykollib.Session", furniture: MeatFurniture) -> None:
        """
            Uses the meat bush in the clan rumpus room.
        """
        super().__init__(session)
        spot, furni = furniture.value

        params = {"action": "click", "spot": spot, "furni": furni}
        self.request = session.request("clan_rumpus.php", params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> int:
        return parsing.meat(html)
