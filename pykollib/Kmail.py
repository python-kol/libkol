from .request import kmail_get, kmail_send
from .util.decorators import logged_in


class Kmail(object):
    "This class represents a user's kmail box"

    def __init__(self, session):
        self.session = session

    @logged_in
    async def get(self):
        return await kmail_get(self.session)

    @logged_in
    async def send(self, recipient, message=""):
        await kmail_send(self.session, recipient, message=message).parse()
