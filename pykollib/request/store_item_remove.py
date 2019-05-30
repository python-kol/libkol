from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from ..Error import ItemNotFoundError
from ..Item import Item
from ..pattern import PatternManager


def parse(html: str, **kwargs) -> bool:
    # First parse for errors
    notEnoughPattern = PatternManager.getOrCompilePattern("dontHaveThatManyInStore")
    if notEnoughPattern.search(html):
        raise ItemNotFoundError("You either don't have that item, or not enough")

    # Check if responseText matches the success pattern. If not, raise error.
    itemTakenSuccessfully = PatternManager.getOrCompilePattern("itemTakenSuccessfully")
    if itemTakenSuccessfully.search(html) is None:
        raise ItemNotFoundError("Something went wrong with the taking of the item.")

    return True


def store_item_remove(
    session: "pykollib.Session", item: Item, quantity: int = 1
) -> Coroutine[Any, Any, ClientResponse]:
    """
    Take a single item from your store using the new Mall interface from Sep 2013

    Class expects at least an itemId. If no quantity is given, a quantity of 1 is assumed

    Todo: add option to remove all of an item. This will require calling StoreInventoryRequest
    and figuring out how many of the item there are.

    :param item: Item to remove
    :param quantity: Amount of that item to remove
    """

    params = {"action": "removeitem", "itemid": item.id, "qty": quantity}
    return session.request("backoffice.php", params=params, parse=parse)
