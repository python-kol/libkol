from aiohttp import ClientResponse
from typing import TYPE_CHECKING, Coroutine, Any

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import Item
from ..Error import UserIsDrunkError, WrongKindOfItemError, ItemNotFoundError
from ..util import parsing


def parse(html: str, **kwargs) -> parsing.ResourceGain:
    if "You're way too drunk already." in html:
        raise UserIsDrunkError("You are too drunk to drink more booze.")

    if "That's not booze." in html:
        raise WrongKindOfItemError("That item is not booze.")

    if ">You don't have the item you're trying to use.<" in html:
        raise ItemNotFoundError("Item not in inventory.")

    # Check the results
    return parsing.resource_gain(html)


def drink(session: "Session", item: Item) -> Coroutine[Any, Any, ClientResponse]:
    """
    This request is for drinking booze from the inventory.
    It accepts the current session and the ID number of the booze to be drank.
    It returns the results, including and stat gain, adventure gain,
    effect gain, or drunkenness gain.
    """
    params = {"which": 1, "whichitem": item.id}
    return session.request(
        "inv_booze.php", ajax=True, pwd=True, params=params, parse=parse
    )
