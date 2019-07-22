from yarl import URL
from typing import Union
import libkol

from .request import Request
from .combat import combat, CombatRound

Response = Union[CombatRound, None]


class adventure(Request[Response]):
    """
    A request used to initiate an adventure at any location.

    :param session: Active Session
    :param location_id: Id of the location in which to adventure
    """

    fight = True

    def __init__(self, session: "libkol.Session", location_id: int):
        super().__init__(session)

        params = {"snarfblat": location_id}
        self.request = session.request("adventure.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> Response:
        url = kwargs["url"]  # type: URL

        if url.path == "/fight.php":
            return await combat.parser(content, **kwargs)

        if url.path == "/choice.php":
            print("We don't support choices yet")

        return None
