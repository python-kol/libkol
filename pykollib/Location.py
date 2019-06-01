from .request import adventure


class Location(object):
    "This class represents a user's kmail box"

    def __init__(self, session, id):
        self.session = session
        self.id = id

    async def visit(self):
        return await self.session.parse(adventure, self.id)
