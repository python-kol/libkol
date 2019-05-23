from aiohttp import ClientResponse
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import Item, ItemQuantity


def parse(json) -> List[ItemQuantity]:
    return [ItemQuantity(Item[id], quantity) for id, quantity in json.items()]


def inventory(session: "Session") -> ClientResponse:
    "This class is used to get a list of items in the user's inventory."
    data = {"for": session.state.get("user_agent", "pykollib"), "what": "inventory"}

    return session.request("api.php", json=True, data=data, parse=parse)
