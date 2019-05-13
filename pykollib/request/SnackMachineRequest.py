from aiohttp import ClientResponse


def snackMachineRequest(session: "Session") -> ClientResponse:
    "Uses the snack machine in the clan rumpus room."

    params["action"] = "click"
    params["spot"] = 9
    params["furni"] = 2

    return session.request("clan_rumpus.php", params=params)

