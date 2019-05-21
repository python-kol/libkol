from aiohttp import ClientResponse
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import ItemQuantity


def clan_stash_item_add(
    session: "Session", items: List[ItemQuantity]
) -> ClientResponse:
    "Adds items to the clan's stash."

    params = {"action": "addgoodies"}

    for i, iq in items.enumerate():
        params["item{}".format(i)] = iq["item"].id
        params["qty{}".format(i)] = iq["quantity"]

    return session.request("clan_stash.php", pwd=True)
