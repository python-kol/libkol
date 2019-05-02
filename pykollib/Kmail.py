from .request import SendMessageRequest


class Kmail(object):
    "This class represents a user's kmail box"

    def __init__(self, session):
        self.session = session

    def send(self, recipient, message=""):
        msg = {"userId": recipient, "text": message}

        SendMessageRequest(self.session, msg).doRequest()
