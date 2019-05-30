from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from ..Item import Item


def closet_item_add(session: "pykollib.Session", item: Item, quantity: int) -> Coroutine[Any, Any, ClientResponse]:
    "Adds items to the player's closet."

    params = {"action": "closetpush", "whichitem": item.id, "qty": quantity, "ajax": 1}
    return session.request("fillcloset.php", pwd=True, params=params)
