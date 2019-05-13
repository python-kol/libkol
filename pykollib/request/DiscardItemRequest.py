from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def discardItemRequest(session: "Session", item_id: int = 0) -> ClientResponse:

    params = {"action": "discard", "whichitem": item_id}
    return session.request("inventory.php", params=params)
