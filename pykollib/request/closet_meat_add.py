from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def closet_meat_add(session: "pykollib.Session", quantity: int) -> Coroutine[Any, Any, ClientResponse]:
    "Adds meat to the player's closet."

    params = {"action": "addmeat", "amt": quantity}
    return session.request("closet.php", pwd=True, params=params)
