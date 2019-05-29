from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def adventure(session: "Session", location_id: int) -> ClientResponse:
    "A request used to initiate an adventure at any location."
    params = {"snarfblat": location_id}

    return session.request("adventure.php", params=params)