from aiohttp import ClientResponse


def jukeboxRequest(session: "Session") -> ClientResponse:
    "Uses the jukebox in the clan rumpus room."

    params["action"] = "click"
    params["spot"] = 3
    params["furni] = 2

    return session.request("clan_rumpus.php", params=params)
