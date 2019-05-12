from aiohttp import ClientResponse

def discardItemRequest(session: "Session", item: "Item" = 0) -> ClientResponse:

    params = {}

    params["action"] = "discard"
    params["whichitem"] = str(item)

    return session.request("inventory.php", params=params)
