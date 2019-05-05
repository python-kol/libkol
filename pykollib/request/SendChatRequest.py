from .GenericRequest import GenericRequest
from pykollib.util import ChatUtils

import time
import unicodedata
import urllib.request, urllib.parse, urllib.error


class SendChatRequest(GenericRequest):
    def __init__(self, session, text):
        super(SendChatRequest, self).__init__(session)
        self.text = text.strip()
        self.url = session.server_url + "submitnewchat.php?playerid=%s&pwd=%s" % (
            session.user_id,
            session.pwd,
        )
        self.url += "&%s" % urllib.parse.urlencode(
            {
                "graf": unicodedata.normalize("NFKD", self.text.decode("utf-8")).encode(
                    "ascii", "ignore"
                )
            }
        )

    def parseResponse(self):
        # Parse the chat messages returned.
        self.responseData["chatMessages"] = ChatUtils.parseOutgoingChatMessages(
            self.responseText
        )
