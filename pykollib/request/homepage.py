from aiohttp import ClientResponse
from typing import TYPE_CHECKING, NamedTuple
from yarl import URL

if TYPE_CHECKING:
    from ..Session import Session


class Response(NamedTuple):
    server_url: str


def parse(url: URL, **kwargs) -> Response:
    return Response(str(url.origin()))


def homepage(session: "Session", server_number: int = 0) -> ClientResponse:
    """
    This request is most often used before logging in. It allows the KoL servers to assign a
    particular server number to the user. In addition, it gives us the user's login challenge
    so that we might login to the server in a more secure fashion.
    """
    if server_number > 0:
        url = "https://www{}.kingdomofloathing.com/main.php".format(server_number)
    else:
        url = "https://www.kingdomofloathing.com/"

    return session.request(url, parse=parse)
