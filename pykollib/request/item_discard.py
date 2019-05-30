from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from ..Item import Item


def item_discard(
    session: "pykollib.Session", item: Item
) -> Coroutine[Any, Any, ClientResponse]:
    params = {"action": "discard", "whichitem": item.id}
    return session.request("inventory.php", params=params)
