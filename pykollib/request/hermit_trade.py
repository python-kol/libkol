from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib

from ..Error import ItemNotFoundError, UnknownError, WrongKindOfItemError
from ..Item import Item, ItemQuantity
from ..util import parsing


def parse(html: str, **kwargs) -> List[ItemQuantity]:
    if (
        "you are able to infer that he doesn't have enough clovers to make that trade"
        in html
    ):
        raise ItemNotFoundError(
            "The Hermit doesn't have enough clovers for that.", item=24
        )

    if "You don't have enough stuff" in html:
        raise ItemNotFoundError(
            "You don't have enough worthless items for that.", item=43
        )

    if "You don't have enough Hermit Permits to trade for that many" in html:
        raise ItemNotFoundError(
            "You don't have enough hermit permits for that.", item=42
        )

    if "The Hermit doesn't have that item" in html:
        raise WrongKindOfItemError("The Hermit doesn't have any of those.")

    if "You make a trade with the Hermit." not in html:
        raise UnknownError("Unknown error")

    return parsing.item(html)


def hermit_trade(
    session: "pykollib.Session", item: Item, quantity: int = 1
) -> Coroutine[Any, Any, ClientResponse]:
    data = {"action": "trade", "quantity": quantity, "whichitem": item.id}
    return session.request("hermit.php", data=data, parse=parse)
