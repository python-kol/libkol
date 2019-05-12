from aiohttp import ClientResponse


def meatTreeRequest(session: "Session") -> ClientResponse:
    "Uses the meat tree in the clan rumpus room."

    params["action"] = "click"
    params["spot"] = 9
    params["furni] = 3

    return session.request("clan_rumpus.php", params=params)

