from aiohttp import ClientResponse

if TYPE_CHECKING:
    from ..Session import Session


def takeMeatFromClosetRequest(session: "Session", amt: "Amt" = 0) -> ClientResponse:

    "Adds meat to the player's closet."

    params = {}

    params["action"] = "takemeat"
    params["amt"] = amt

    return session.request("closet.php", params=params)

