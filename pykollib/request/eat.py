from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from ..Error import ItemNotFoundError, UserIsDrunkError, WrongKindOfItemError
from ..Item import Item
from ..util import parsing


def parse(html: str, **kwargs) -> parsing.ResourceGain:
    if "You're way too drunk already." in html:
        raise UserIsDrunkError("You're too full to eat that.")

    if "That's not booze." in html:
        raise WrongKindOfItemError("That's not something you can eat.")

    if ">You don't have the item you're trying to use.<" in html:
        raise ItemNotFoundError("Item not in inventory.")

    # Check the results
    return parsing.resource_gain(html)


def eat(session: "pykollib.Session", item: Item) -> Coroutine[Any, Any, ClientResponse]:
    """
    This request is for eating food from the inventory.
    It accepts the current session and the ID number of the food to eat.
    It returns the results, including and stat gain, adventure gain, or effect gain.
    """
    params = {"which": 1, "whichitem": item.id}
    return session.request(
        "inv_eat.php", ajax=True, pwd=True, params=params, parse=parse
    )
