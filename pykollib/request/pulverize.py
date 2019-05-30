from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib

from ..Error import ItemNotFoundError, WrongKindOfItemError
from ..Item import Item, ItemQuantity
from ..util import parsing


def parse(html: str, **yargs) -> List[ItemQuantity]:
    if "<td>That's not something you can pulverize.</td>" in html:
        raise WrongKindOfItemError("That item cannot be pulverized")

    if "<td>You haven't got that many" in html:
        raise ItemNotFoundError("Not enough of that item")

    return parsing.item(html)


def pulverize(session: "pykollib.Session", item: Item, quantity: int = 1) -> Coroutine[Any, Any, ClientResponse]:
    params = {
        "action": "pulverize",
        "mode": "smith",
        "smashitem": item.id,
        "qty": quantity,
    }

    return session.request("craft.php", pwd=True, params=params, parse=parse)
