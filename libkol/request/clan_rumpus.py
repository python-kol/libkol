import re
from enum import Enum
from typing import List

import libkol

from .request import Request


class Furniture(Enum):
    Nail = (1, 0)
    GirlsCalendar = (1, 1)
    BoyCalendar = (1, 2)
    Painting = (1, 3)
    MeatOrchid = (1, 4)
    Bookshelf = (2, 0)
    ArcaneTomes = (2, 1)
    SportsMemorabilia = (2, 2)
    SelfHelpBooks = (2, 3)
    Outlet = (3, 0)
    SodaMachine = (3, 1)
    Jukebox = (3, 2)
    MrKlaw = (3, 3)
    Endtable = (4, 0)
    Radio = (4, 1)
    MeatBush = (4, 2)
    InspirationalCalendar = (4, 3)
    Rug = (5, 0)
    WrestlingMat = (5, 1)
    TanningBed = (5, 2)
    ComfySofa = (5, 3)
    Corner = (9, 0)
    HoboFlex = (9, 1)
    SnackMachine = (9, 2)
    MeatTree = (9, 3)

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


furniture_pattern = re.compile(r"rump([0-9])_([0-9])\.gif")


class clan_rumpus(Request[List[Furniture]]):
    def __init__(self, session: "libkol.Session"):
        super().__init__(session)
        self.request = session.request("clan_rumpus.php")

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Furniture]:
        return [
            Furniture(coords)
            for coords in (
                (f.group(1), f.group(2)) for f in furniture_pattern.finditer(content)
            )
            if Furniture.has_value(coords)
        ]
