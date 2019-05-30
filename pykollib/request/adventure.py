from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def adventure(session: "pykollib.Session", location_id: int) -> Coroutine[Any, Any, ClientResponse]:
    "A request used to initiate an adventure at any location."
    params = {"snarfblat": location_id}

    return session.request("adventure.php", params=params)
