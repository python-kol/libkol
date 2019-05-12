from aiohttp import ClientResponse


def useItemRequest(session: "Session", itemId: "itemId" = None) -> ClientResponse:

    """
    Uses the requested item.
    """

    params={'whichitem': str(itemId)}
    return session.request("inv_use.php", params=pararms)
