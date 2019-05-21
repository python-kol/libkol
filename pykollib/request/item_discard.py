from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import Item


def item_discard(session: "Session", item: Item) -> ClientResponse:
    params = {"action": "discard", "whichitem": item.id}
    return session.request("inventory.php", params=params)
