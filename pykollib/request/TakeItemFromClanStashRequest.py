from aiohttp import ClientResponse

def unequipRequest(session: "Session", itemId: "itemId" = 0, quantity: "quantity" = 0) -> ClientResponse:
    "Take items from the player's clan stash."

    params = {}

    params["action"] = "takegoodies"
    params["whichitem"] = itemId
    params["quantity"] = quantity

    return session.request("clan_stash.php", params=params)
