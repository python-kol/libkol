from GenericRequest import GenericRequest
from pykollib.manager import PatternManager
from pykollib.util import ChatUtils
from pykollib.util import Report
from pykollib.util import StringUtils

class GetChatMessagesRequest(GenericRequest):
    def __init__(self, session, lastTime=0):
        super(GetChatMessagesRequest, self).__init__(session)
        self.url = session.serverURL + "newchatmessages.php?lasttime=%s" % lastTime

    def parseResponse(self):
        # Get the timestamp we should send to the server next time we make a request.
        lastSeenPattern = PatternManager.getOrCompilePattern("chatLastSeen")
        match = lastSeenPattern.search(self.responseText)
        self.responseData["lastSeen"] = match.group(1)

        # Parse the chat messages.
        text = self.responseText[:self.responseText.find('<!--lastseen')]
        self.responseData["chatMessages"] = ChatUtils.parseIncomingChatMessage(self.responseText)