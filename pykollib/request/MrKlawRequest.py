from aiohttp import ClientResponse


def mrKlawRequest(session: "Session") -> ClientResponse:
    "Uses the Mr. Klaw in the clan rumpus room."

    params["action"] = "click"
    params["spot"] = 3
    params["furni] = 3

    return session.request("clan_rumpus.php", params=params)

