from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def status(session: "Session") -> ClientResponse:
    payload = {"for": session.state.get("user_agent", "pykollib"), "what": "status"}

    return session.request("api.php", json=True, data=payload)
