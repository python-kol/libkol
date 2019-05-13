from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def takeItemFromClanStashRequest(
    session: "Session", item_id: int = 0, quantity: int = 0
) -> ClientResponse:
    "Take items from the player's clan stash."

    params = {"action": "takegoodies", "whichitem": item_id, "quantity": quantity}
    return session.request("clan_stash.php", params=params)
