from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def closet_meat_remove(session: "pykollib.Session", amount: int = 0) -> Coroutine[Any, Any, ClientResponse]:
    "Takes meat from the player's closet."

    params = {"action": "takemeat", "amt": amount}
    return session.request("closet.php", params=params)
