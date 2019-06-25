from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple
from bs4 import BeautifulSoup

import libkol

from .request import Request
from ..Error import NotEnoughHPError, InvalidLocationError, InvalidOutfitError
from ..util import parsing


class MiningSpotType(Enum):
    Promising = "Promising"
    Open = "Open"
    Rocky = "Rocky"


@dataclass
class Response:
    mine: List[List[MiningSpotType]]
    resource_gain: parsing.ResourceGain


class mining(Request[Response]):
    """
    A request used to mine a mine.

    :param session: Active Session
    :param location_id: Id of the mine to visit
    :param x: x coordinate of 6x6 mine (left to right)
    :param y: y coordinate of 6x6 mine (bottom to top)
    """

    def __init__(
        self,
        session: "libkol.Session",
        mine: int,
        reset: bool = False,
        coords: Optional[Tuple[int, int]] = None,
    ):
        super().__init__(session)

        params = {"mine": mine}

        if reset:
            params["reset"] = 1
        if coords is not None:
            # Convert our coordinates to kol coordinates
            x, y = coords
            params["which"] = x + 1 + (8 * (6 - y))

        self.request = session.request("mining.php", pwd=True, params=params)

    @staticmethod
    def parse_mine(content: str) -> List[List[MiningSpotType]]:
        soup = BeautifulSoup(content, "html.parser")

        m = [[MiningSpotType.Open] * 6 for i in range(6)]

        for spot in soup.find_all("img", width="50", height="50"):
            alt = spot["alt"]
            spot_type = MiningSpotType(alt[0 : alt.find(" ")])
            x, y = [int(i) for i in alt[-4:-1].split(",")]

            if x not in [0, 7] and y not in [0, 7]:
                m[x - 1][6 - y] = spot_type

        return m

    @classmethod
    async def parser(cls, content: str, **kwargs) -> Response:
        if "<td>You're way too beaten up to mine right now." in content:
            raise NotEnoughHPError("You need HP to mine")

        if "<td>That's not a valid mine.</td>" in content:
            raise InvalidLocationError("Mine not found or cannot be accessed")

        if "<td>You can't mine without the proper equipment" in content:
            raise InvalidOutfitError("Incorrect outfit")

        if "<td>You wander around randomly in the mine" not in content:
            session = kwargs["session"]  # type: libkol.Session
            session.state["adventures"] -= 1

        mine = cls.parse_mine(content)

        return Response(mine=mine, resource_gain=await parsing.resource_gain(content))
