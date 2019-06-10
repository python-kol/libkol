import re
from dataclasses import dataclass
from typing import Any, Dict, List

import libkol

from ..Error import UnknownError
from .request import Request

last_seen_pattern = re.compile(r"lastseen:([0-9]+)")


@dataclass
class Response:
    msgs: List[str]
    last: int
    delay: int


class chat_receive(Request[Response]):
    returns_json = True

    def __init__(self, session: "libkol.Session", since: int = 0) -> None:
        super().__init__(session)
        params = {
            # "aa" is a float and I don't know what it means but it works without it
            "j": 1,
            "lasttime": since,
        }
        self.request = session.request("newchatmessages.php", params=params)

    @staticmethod
    async def parser(content: Dict[str, Any], **kwargs) -> Response:
        try:
            return Response(**content)
        except TypeError:
            raise UnknownError("Unknown response from receiving chat messages")
