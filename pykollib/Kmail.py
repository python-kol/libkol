from .request import SendMessageRequest, getMessagesRequest
from .util.decorators import logged_in


class Kmail(object):
    "This class represents a user's kmail box"

    def __init__(self, session):
        self.session = session

    @logged_in
    async def get(self):
        s = self.session
        return await (await getMessagesRequest(s)).parse()

    @logged_in
    def send(self, recipient, message=""):
        msg = {"userId": recipient, "text": message}

        SendMessageRequest(self.session, msg).doRequest()
