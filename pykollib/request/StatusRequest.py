from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def statusRequest(session: "Session") -> ClientResponse:
    payload = {"for": session.preferences["userAgent"], "what": "status"}

    return session.request("api.php", data=payload)
