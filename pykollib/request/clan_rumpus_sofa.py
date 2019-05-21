from aiohttp import ClientResponse
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..util import parsing


class Response(NamedTuple):
    mp: int
    hp: int


def parse(html: str, **kwargs) -> Response:
    return Response(parsing.mp(html), parsing.hp(html))


def clan_rumpus_sofa(session: "Session", turns: int = 0) -> ClientResponse:
    """
    Uses the comfy sofa in the clan rumpus room.
    """

    params = {"preaction": "nap", "numturns": turns}
    return session.request("clan_rumpus.php", params=params, parse=parse)
