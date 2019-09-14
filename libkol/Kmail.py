from typings import List, Union

from . import request
from .util.decorators import logged_in


class Kmail:
    "This class represents a user's kmail box"

    def __init__(self, session):
        self.session = session

    @logged_in
    async def get(self):
        return await request.kmail_get(self.session).parse()

    @logged_in
    async def send(self, recipient, message="", meat: int = 0):
        return await request.kmail_send(
            self.session, recipient, message=message, meat=meat
        ).parse()

    @logged_in
    async def delete(self, message_id: Union[int, List[int]], box: str = "Inbox"):
        if isinstance(message_id, int):
            message_id = [message_id]

        return await request.kmail_delete(self.session, message_id, box).parse()
