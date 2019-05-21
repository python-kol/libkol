from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def clan_stash_meat_add(session: "Session", quantity: int) -> ClientResponse:
    "Adds meat to the player's clan stash."

    params = {"action": "contribute", "howmuch": quantity}
    return session.request("clan_stash.php", pwd=True, params=params)
