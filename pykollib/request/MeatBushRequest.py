from aiohttp import ClientResponse


def meatBushRequest(session: "Session") -> ClientResponse:
    "Uses the meat bush in the clan rumpus room."

    params["action"] = "click"
    params["spot"] = 4
    params["furni"] = 2

    return session.request("clan_rumpus.php", params=params)

