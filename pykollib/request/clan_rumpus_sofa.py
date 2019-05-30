from typing import Any, Coroutine, NamedTuple

from aiohttp import ClientResponse

import pykollib

from ..util import parsing


class Response(NamedTuple):
    mp: int
    hp: int


def parse(html: str, **kwargs) -> Response:
    return Response(parsing.mp(html), parsing.hp(html))


def clan_rumpus_sofa(session: "pykollib.Session", turns: int = 0) -> Coroutine[Any, Any, ClientResponse]:
    """
    Uses the comfy sofa in the clan rumpus room.
    """

    params = {"preaction": "nap", "numturns": turns}
    return session.request("clan_rumpus.php", params=params, parse=parse)
