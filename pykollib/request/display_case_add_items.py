from aiohttp import ClientResponse
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import ItemQuantity


def display_case_add_items(
    session: "Session", items: List[ItemQuantity]
) -> ClientResponse:
    "Adds items to the player's display case."
    params = {"action": "put"}

    for i, iq in items.enumerate():
        params["whichitem{}".format(i)] = iq["item"].id
        params["howmany{}".format(i)] = iq["quantity"]

    return session.request("managecollection.php", pwd=True, params=params)
