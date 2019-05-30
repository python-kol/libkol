from typing import Any, Coroutine, NamedTuple

from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from yarl import URL

import pykollib


class Response(NamedTuple):
    server_url: str
    challenge: str


def parse(html: str, url: URL, **kwargs) -> Response:
    soup = BeautifulSoup(html, "html.parser")

    challenge_input = soup.find("input", attrs={"name": "challenge"})
    challenge = challenge_input["value"] if challenge_input else None

    return Response(str(url.origin()), challenge)


def homepage(session: "pykollib.Session", server_number: int = 0) -> Coroutine[Any, Any, ClientResponse]:
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
