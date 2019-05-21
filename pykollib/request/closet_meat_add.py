from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def closet_meat_add(session: "Session", quantity: int) -> ClientResponse:
    "Adds meat to the player's closet."

    params = {"action": "addmeat", "amt": quantity}
    return session.request("closet.php", pwd=True, params=params)
