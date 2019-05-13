from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def useItemRequest(session: "Session", item_id: int = None) -> ClientResponse:
    """
    Uses the requested item.
    """

    params = {"whichitem": item_id}
    return session.request("inv_use.php", params=params)
