from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def useItemRequest(session: "Session", itemId: "itemId" = None) -> ClientResponse:

    """
    Uses the requested item.
    """

    params={'whichitem': str(itemId)}
    return session.request("inv_use.php", params=pararms)
