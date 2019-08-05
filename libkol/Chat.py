import asyncio
from typing import AsyncIterator, List

from .request import chat_channel, chat_send, chat_receive
from .util.decorators import logged_in


class Chat:
    "This class represents KoL chat"

    def __init__(self, session):
        self.session = session

    @logged_in
    async def get_channel(self):
        return await chat_channel(self.session).parse()

    @logged_in
    async def messages(
        self, since: int = 0, delay: int = 10
    ) -> AsyncIterator[List[str]]:
        while True:
            data = await chat_receive(self.session, since).parse()
            since = data.last
            yield data.msgs
            await asyncio.sleep(delay)

    @logged_in
    async def send(self, recipient, message: str = ""):
        await chat_send(self.session, text=message).parse()
