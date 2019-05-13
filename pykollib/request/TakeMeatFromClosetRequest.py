from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def takeMeatFromClosetRequest(session: "Session", amount: int = 0) -> ClientResponse:
    "Takes meat from the player's closet."

    params = {"action": "takemeat", "amt": amount}
    return session.request("closet.php", params=params)
