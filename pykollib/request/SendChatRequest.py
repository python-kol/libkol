import unicodedata
import urllib.error
import urllib.parse
import urllib.request

from pykollib.util import ChatUtils

from .GenericRequest import GenericRequest


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

    async def parseresponse(self):
        # Parse the chat messages returned.
        self.responseData["chatMessages"] = ChatUtils.parseOutgoingChatMessages(
            self.responseText
        )
