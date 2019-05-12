from aiohttp import ClientResponse


def takeMeatFromClosetRequest(session: "Session", amt: "Amt" = 0) -> ClientResponse:

    "Takes meat to the player's closet."

    params = {}

    params["action"] = "takemeat"
    params["amt"] = amt

    return session.request("closet.php", params=params)

