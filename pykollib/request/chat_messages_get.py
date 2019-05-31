import re
from typing import Any, Dict, List, NamedTuple

import pykollib

from ..Error import UnknownError
from ..util import ChatUtils
from .request import Request

last_seen_pattern = re.compile(r"lastseen:([0-9]+)")


class Response(NamedTuple):
    last_seen: int
    messages: List[Dict[str, Any]]


class chat_messages_get(Request):
    def __init__(self, session: "pykollib.Session", since: int = 0) -> None:
        super().__init__(session)
        params = {"lasttime": since}
        self.request = session.request("newchatmessages.php", params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> Response:
        # Get the timestamp we should send to the server next time we make a request.
        last_seen_matcher = last_seen_pattern.search(html)

        if last_seen_matcher is None:
            raise UnknownError("Could not parse last seen comment in chat")

        last_seen = int(last_seen_matcher.group(1))

        html = html[: html.find("<!--lastseen")]
        return Response(last_seen, ChatUtils.parseIncomingChatMessage(html))
