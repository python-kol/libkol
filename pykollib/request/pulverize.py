from aiohttp import ClientResponse
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Session import Session

from ..Error import WrongKindOfItemError, ItemNotFoundError
from ..Item import Item, ItemQuantity
from ..util import parsing


def parse(html: str, **yargs) -> List[ItemQuantity]:
    if "<td>That's not something you can pulverize.</td>" in html:
        raise WrongKindOfItemError("That item cannot be pulverized")

    if "<td>You haven't got that many" in html:
        raise ItemNotFoundError("Not enough of that item")

    return parsing.item(html)


def pulverize(session: "Session", item: Item, quantity: int = 1) -> ClientResponse:
    params = {
        "action": "pulverize",
        "mode": "smith",
        "smashitem": item.id,
        "qty": quantity,
    }

    return session.request("craft.php", pwd=True, params=params, parse=parse)
