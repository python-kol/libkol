from .request import adventureRequest


class Location(object):
    "This class represents a user's kmail box"

    def __init__(self, session, id):
        self.session = session
        self.id = id

    async def visit(self):
        s = self.session
        return await adventureRequest(s, self.id)
