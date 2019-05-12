from aiohttp import ClientResponse


def oldTimeyRadioRequest(session: "Session") -> ClientResponse:
    "Uses the Old-Timey Radio in the clan rumpus room."

    params["action"] = "click"
    params["spot"] = 4
    params["furni] = 1

    return session.request("clan_rumpus.php", params=params)

