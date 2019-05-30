from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib

from ..Item import Item, ItemQuantity


def parse(json) -> List[ItemQuantity]:
    return [ItemQuantity(Item[id], quantity) for id, quantity in json.items()]


def inventory(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    "This class is used to get a list of items in the user's inventory."
    data = {"for": session.state.get("user_agent", "pykollib"), "what": "inventory"}

    return session.request("api.php", json=True, data=data, parse=parse)
