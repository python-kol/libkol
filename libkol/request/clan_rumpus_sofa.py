from typing import NamedTuple

import libkol

from ..util import parsing
from .request import Request


class Response(NamedTuple):
    mp: int
    hp: int


class clan_rumpus_sofa(Request[Response]):
    """
    Uses the comfy sofa in the clan rumpus room.
    """

    def __init__(self, session: "libkol.Session", turns: int = 0) -> None:
        super().__init__(session)

        params = {"preaction": "nap", "numturns": turns}
        self.request = session.request("clan_rumpus.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> Response:
        return Response(parsing.mp(content), parsing.hp(content))
