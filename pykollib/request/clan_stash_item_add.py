from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib

from ..Item import ItemQuantity


def clan_stash_item_add(
    session: "pykollib.Session", items: List[ItemQuantity]
) -> Coroutine[Any, Any, ClientResponse]:
    "Adds items to the clan's stash."

    params = {"action": "addgoodies"}

    for i, iq in enumerate(items):
        params["item{}".format(i)] = iq["item"].id
        params["qty{}".format(i)] = iq["quantity"]

    return session.request("clan_stash.php", pwd=True)
