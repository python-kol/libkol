from enum import Enum

import libkol

from ..util import parsing
from .clan_rumpus import Furniture
from .request import Request


class MeatFurniture(Enum):
    Orchid = Furniture.MeatOrchid
    Tree = Furniture.MeatTree
    Bush = Furniture.MeatBush


class clan_rumpus_meat(Request[int]):
    """
    Uses a meat dispenser in the clan rumpus room.
    """

    def __init__(self, session: "libkol.Session", furniture: MeatFurniture) -> None:
        super().__init__(session)
        spot, furni = furniture.value

        params = {"action": "click", "spot": spot, "furni": furni}
        self.request = session.request("clan_rumpus.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> int:
        return parsing.meat(content)
