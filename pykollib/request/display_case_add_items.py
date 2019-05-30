from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib

from ..Item import ItemQuantity


def display_case_add_items(
    session: "pykollib.Session", items: List[ItemQuantity]
) -> Coroutine[Any, Any, ClientResponse]:
    "Adds items to the player's display case."
    params = {"action": "put"}

    for i, iq in items.enumerate():
        params["whichitem{}".format(i)] = iq["item"].id
        params["howmany{}".format(i)] = iq["quantity"]

    return session.request("managecollection.php", pwd=True, params=params)
