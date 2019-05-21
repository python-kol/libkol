from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import Item


def closet_item_add(session: "Session", item: Item, quantity: int) -> ClientResponse:
    "Adds items to the player's closet."

    params = {"action": "closetpush", "whichitem": item.id, "qty": quantity, "ajax": 1}
    return session.request("fillcloset.php", pwd=True, params=params)
