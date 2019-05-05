from .request import SendMessageRequest, getMessagesRequest


class Kmail(object):
    "This class represents a user's kmail box"

    def __init__(self, session):
        self.session = session

    async def get(self):
        s = self.session
        return await (await getMessagesRequest(s)).parse()

    def send(self, recipient, message=""):
        msg = {"userId": recipient, "text": message}

        SendMessageRequest(self.session, msg).doRequest()
