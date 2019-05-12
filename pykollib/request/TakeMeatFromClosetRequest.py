from aiohttp import ClientResponse

if TYPE_CHECKING:
    from ..Session import Session


class TakeMeatFromClosetRequest(GenericRequest):
    "Adds meat to the player's closet."

    def __init__(self, session, meat=""):
        super(TakeMeatFromClosetRequest, self).__init__(session)
        self.url = session.server_url + "closet.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "takemeat"
        self.requestData["amt"] = meat

def takeMeatFromClosetRequest(session: "Session", amt: "Amt" = 0) -> ClientResponse:

    "Adds meat to the player's closet."

    params = {}

    params["action"] = "takemeat"
    params["amt"] = amt

    return session.request("closet.php", params=params)

