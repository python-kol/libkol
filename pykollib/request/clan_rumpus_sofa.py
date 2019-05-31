from typing import NamedTuple

from .request import Request

import pykollib

from ..util import parsing


class Response(NamedTuple):
    mp: int
    hp: int

class clan_rumpus_sofa(Request):
    def __init__(self, session: "pykollib.Session", turns: int = 0) -> None:
        """
        Uses the comfy sofa in the clan rumpus room.
        """

        super().__init__(session)

        params = {"preaction": "nap", "numturns": turns}
        self.request = session.request("clan_rumpus.php", params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> Response:
        return Response(parsing.mp(html), parsing.hp(html))
