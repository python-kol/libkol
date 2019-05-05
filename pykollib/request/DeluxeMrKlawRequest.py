from .GenericRequest import GenericRequest
from pykollib.util import ParseResponseUtils


class DeluxeMrKlawRequest(GenericRequest):
    "Uses the Deluxe Mr. Klaw in the clan VIP room."

    def __init__(self, session):
        super(DeluxeMrKlawRequest, self).__init__(session)
        self.url = session.server_url + "clan_viplounge.php"
        self.requestData["action"] = "klaw"

    def parseResponse(self):
        self.responseData["items"] = ParseResponseUtils.parseItemsReceived(
            self.responseText, self.session
        )
