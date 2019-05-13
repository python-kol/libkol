from aiohttp import ClientResponse
from typing import TYPE_CHECKING
from time import time

from ..Error import ItemNotFoundError
from ..pattern import PatternManager

if TYPE_CHECKING:
    from ..Session import Session


def parse(html: str, **kwargs) -> bool:
    # First parse for errors
    notEnoughPattern = PatternManager.getOrCompilePattern("dontHaveEnoughOfItem")
    if notEnoughPattern.search(html):
        raise ItemNotFoundError("You don't have that many of that item.")

    dontHaveItemPattern = PatternManager.getOrCompilePattern("dontHaveThatItem")
    if dontHaveItemPattern.search(html):
        raise ItemNotFoundError("You don't have that item.")

    # Check if responseText matches the success pattern. If not, raise error.
    itemAddedSuccessfully = PatternManager.getOrCompilePattern("itemAddedSuccessfully")
    if itemAddedSuccessfully.search(html):
        return True
    else:
        raise ItemNotFoundError("Something went wrong with the adding.")


def addItemToStoreRequest(
    session: "Session",
    item_id: int,
    quantity: int = 1,
    limit: int = "",
    price: int = 999999999,
    from_hangks: bool = False,
) -> ClientResponse:
    """
    Add a single item to your store. The interface to the mall was updated on Sept 13, 2013.
    It looks like items are now added only one at a time.

    Notes about new URL: http://www.kingdomofloathing.com/backoffice.php
    itemid: this will contain an "h" in front of it if the item is in Hangk's

    There is now a submitted field name '_'. This appears to be the milliseconds since epoch.
    Testing will need to be done to see how important this is. Presumably you could just append
    000 after the current seconds since epoch.
    """

    params = {
        "action": "additem",
        "_": int(time() * 1000),
        "ajax": 1,
        "itemid": item_id if from_hangks is False else "h{}".format(item_id),
        "price": price,
        "limit": limit,
        "quantity": quantity,
    }

    return session.request("backoffice.php", pwd=True, params=params, parse=parse)
