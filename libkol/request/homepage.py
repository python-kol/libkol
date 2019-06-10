from typing import NamedTuple, Optional

from bs4 import BeautifulSoup
from yarl import URL

import libkol

from .request import Request


class Response(NamedTuple):
    server_url: str
    challenge: Optional[str]


class homepage(Request[Response]):
    """
    This request is most often used before logging in. It allows the KoL servers to assign a
    particular server number to the user. In addition, it gives us the user's login challenge
    so that we might login to the server in a more secure fashion.
    """

    def __init__(self, session: "libkol.Session", server_number: int = 0) -> None:
        super().__init__(session)

        if server_number > 0:
            url = "https://www{}.kingdomofloathing.com/main.php".format(server_number)
        else:
            url = "https://www.kingdomofloathing.com/"

        self.request = session.request(url)

    @staticmethod
    async def parser(content: str, **kwargs) -> Response:
        url = kwargs["url"]  # type: URL

        soup = BeautifulSoup(content, "html.parser")

        challenge_input = soup.find("input", attrs={"name": "challenge"})
        challenge = str(challenge_input["value"]) if challenge_input else None

        return Response(str(url.origin()), challenge)
