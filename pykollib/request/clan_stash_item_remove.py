from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def clan_stash_item_remove(
    session: "pykollib.Session", item_id: int = 0, quantity: int = 0
) -> Coroutine[Any, Any, ClientResponse]:
    "Take items from the player's clan stash."

    params = {"action": "takegoodies", "whichitem": item_id, "quantity": quantity}
    return session.request("clan_stash.php", params=params)
