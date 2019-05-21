from .GenericRequest import GenericRequest
from pykollib.util import parsing


class LookingGlassRequest(GenericRequest):
    "Uses the Looking Glass in the clan VIP room."

    def __init__(self, session):
        super(LookingGlassRequest, self).__init__(session)
        self.url = session.server_url + "clan_viplounge.php"
        self.requestData["action"] = "lookingglass"

    def parseResponse(self):
        self.responseData["items"] = parsing.parseItemsReceived(
            self.responseText, self.session
        )
