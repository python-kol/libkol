from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import Item


def item_use(session: "Session", item: Item) -> ClientResponse:
    """
    Uses the requested item.
    """

    params = {"whichitem": item.id}
    return session.request("inv_use.php", params=params)
