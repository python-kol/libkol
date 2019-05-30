from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def status(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    payload = {"for": session.state.get("user_agent", "pykollib"), "what": "status"}

    return session.request("api.php", json=True, data=payload)
