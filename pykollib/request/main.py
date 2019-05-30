from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def main(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    return session.request("main.php")
