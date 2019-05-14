import pykollib.Error as Error
from .GenericRequest import GenericRequest

import json


class ApiRequest(GenericRequest):
    def __init__(self, session):
        super(ApiRequest, self).__init__(session)
        self.url = session.server_url + "api.php"

        # Create a user agent string.
        userAgent = session.state.get("user_agent", "pykollib")
        self.requestData["for"] = userAgent

    def parseResponse(self):
        self.jsonData = json.loads(self.responseText)
        if type(self.jsonData) == str or type(self.jsonData) == str:
            raise Error.Error(self.jsonData, Error.REQUEST_GENERIC)
