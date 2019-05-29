from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from typing import List, Any, TYPE_CHECKING, Coroutine, NamedTuple

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import Item


class Listing(NamedTuple):
    price: int
    quantity: int
    limit: int


class Response(NamedTuple):
    unlimited: List[Listing]
    limited: List[Listing]


def parse(html: str, **kwargs):
    soup = BeautifulSoup(html, "html.parser")

    unlimited = soup.find("td", text="unlimited:")
    limited = soup.find("td", text="limited:")

    response = {
        "unlimited": [
            Listing(int(p.b.string.replace(",", "")), int(p.contents[1][2:]), 0)
            for p in unlimited.find_next_siblings("td")
        ],
        "limited": [
            Listing(
                int(p.b.string.replace(",", "")),
                int(p.contents[1].split(" ")[1][1:]),
                int(p.contents[1].split(" ")[0][1:-5]),
            )
            for p in limited.find_next_siblings("td")
        ],
    }

    return Response(**response)


def mall_search_price(
    session: "Session", item: Item
) -> Coroutine[Any, Any, ClientResponse]:
    """
    Search the mall for the lowest prices of an item. This will return the
    4 lowest unlimited prices, and if applicable, the 3 lowest limited
    prices with their limit amount per day.

    I'm not sure what the counts when doing a search are, but I'm including it anyways.
    """
    data = {"action": "prices", "iid": item.id}
    return session.request("backoffice.php", data=data, pwd=True, parse=parse)
