from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def main(session: "Session") -> ClientResponse:
    return session.request("main.php")
