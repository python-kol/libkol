from aiohttp import ClientResponse


def meatOrchidRequest(session: "Session") -> ClientResponse:
    "Uses the hanging meat orchid in the clan rumpus room."

    params["action"] = "click"
    params["spot"] = 1
    params["furni] = 4

    return session.request("clan_rumpus.php", params=params)

