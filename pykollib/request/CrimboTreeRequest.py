from .GenericRequest import GenericRequest
from pykollib.util import ParseResponseUtils


class CrimboTreeRequest(GenericRequest):
    "Uses the Crimbo Tree in the clan VIP room."

    def __init__(self, session):
        super(CrimboTreeRequest, self).__init__(session)
        self.url = session.server_url + "clan_viplounge.php"
        self.requestData["action"] = "crimbotree"

    def parseResponse(self):
        self.responseData["items"] = ParseResponseUtils.parseItemsReceived(
            self.responseText, self.session
        )
