import re

import libkol

from ..Error import UnknownError
from .request import Request

current_channel_pattern = re.compile(
    '<font color="?#?\w+"?>Currently in channel: ([^<>]+)<'
)


class chat_channel(Request[str]):
    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)
        self.request = session.request("lchat.php")

    @staticmethod
    async def parser(content: str, **kwargs) -> str:
        match = current_channel_pattern.search(content)

        if match is None:
            raise UnknownError("Could not parse chat channel")

        return match.group(1)
