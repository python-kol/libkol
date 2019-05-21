from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Error import NotEnoughItemsError, WrongKindOfItemError
from ..Item import Item
from ..util import parsing


def parse(html: str, **kwargs) -> parsing.ResourceGain:
    if (
        "<table><tr><td>You don't have that many of that item.</td></tr></table>"
        in html
    ):
        raise NotEnoughItemsError("You don't have that many of that item.")

    if "<table><tr><td>That item isn't usable in quantity.</td></tr></table>" in html:
        raise WrongKindOfItemError("You cannot multi-use that item.")

    # Find out what happened
    return parsing.resource_gain(html)


def item_multi_use(session: "Session", item: Item, quantity: int) -> ClientResponse:
    "Uses multiple items at once"

    params = {"action": "useitem", "whichitem": item.id, "quantity": quantity}
    return session.request("multiuse.php", pwd=True, params=params, parse=parse)
