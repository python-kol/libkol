from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def statusRequest(session: "Session") -> ClientResponse:
    payload = {"for": session.status.get("user_agent", "pykollib"), "what": "status"}

    return session.request("api.php", data=payload)
