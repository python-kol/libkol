from .request import kmail_send, kmail_get
from .util.decorators import logged_in


class Kmail(object):
    "This class represents a user's kmail box"

    def __init__(self, session):
        self.session = session

    @logged_in
    async def get(self):
        return await self.session.parse(kmail_get)

    @logged_in
    async def send(self, recipient, message=""):
        await self.session.parse(kmail_send, recipient, message=message)
