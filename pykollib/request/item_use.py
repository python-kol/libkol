from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from ..Item import Item


def item_use(session: "pykollib.Session", item: Item) -> Coroutine[Any, Any, ClientResponse]:
    """
    Uses the requested item.
    """

    params = {"whichitem": item.id}
    return session.request("inv_use.php", params=params)
