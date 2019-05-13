from aiohttp import ClientResponse


def sodaMachineRequest(session: "Session") -> ClientResponse:
    "Uses the soda machine in the clan rumpus room."

    params["action"] = "click"
    params["spot"] = 3
    params["furni"] = 1

    return session.request("clan_rumpus.php", params=params)
