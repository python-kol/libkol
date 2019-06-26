from typing import List

from bs4 import BeautifulSoup
from dataclasses import dataclass

import libkol

from .request import Request


@dataclass
class Response:
    unlimited: List["libkol.types.Listing"]
    limited: List["libkol.types.Listing"]


class mall_price(Request[Response]):
    """
    Search the mall for the lowest prices of an item. This will return the
    4 lowest unlimited prices, and if applicable, the 3 lowest limited
    prices with their limit amount per day.

    I'm not sure what the counts when doing a search are, but I'm including it anyways.

    :param session: Active session
    :param item: Item for which to get prices
    """

    def __init__(self, session: "libkol.Session", item: "libkol.Item") -> None:
        super().__init__(session)

        data = {"action": "prices", "iid": item.id}
        self.request = session.request("backoffice.php", data=data, pwd=True)

    @staticmethod
    async def parser(content: str, **kwargs) -> Response:
        from libkol.types import Listing

        soup = BeautifulSoup(content, "html.parser")

        unlimited = soup.find("td", text="unlimited:")
        limited = soup.find("td", text="limited:")

        return Response(
            unlimited=[
                Listing(
                    price=int(p.b.string.replace(",", "")), stock=int(p.contents[1][2:])
                )
                for p in unlimited.find_next_siblings("td")
            ],
            limited=[
                Listing(
                    price=int(p.b.string.replace(",", "")),
                    stock=int(p.contents[1].split(" ")[1][1:]),
                    limit=int(p.contents[1].split(" ")[0][1:-5]),
                )
                for p in limited.find_next_siblings("td")
            ],
        )
