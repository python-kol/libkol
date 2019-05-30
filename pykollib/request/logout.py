from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


async def logout(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    response = await session.request("logout.php")
    session.is_connected = False
    return response
