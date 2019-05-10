from aiohttp import ClientResponse

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


async def logoutRequest(session: "Session") -> ClientResponse:
    response = await session.request("logout.php")
    session.is_connected = False
    return response
