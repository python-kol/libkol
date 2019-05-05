from aiohttp import ClientResponse

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


async def statusRequest(session: "Session") -> ClientResponse:
    payload = {"for": session.preferences["userAgent"], "what": "status"}

    return await session.post("api.php", data=payload)
