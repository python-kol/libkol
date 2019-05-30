from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def clan_stash_meat_add(session: "pykollib.Session", quantity: int) -> Coroutine[Any, Any, ClientResponse]:
    "Adds meat to the player's clan stash."

    params = {"action": "contribute", "howmuch": quantity}
    return session.request("clan_stash.php", pwd=True, params=params)
