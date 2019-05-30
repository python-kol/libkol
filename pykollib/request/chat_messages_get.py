import re
from typing import Any, Coroutine, Dict, List, NamedTuple

from aiohttp import ClientResponse

import pykollib

from ..util import ChatUtils

last_seen_pattern = re.compile(r"lastseen:([0-9]+)")


class Response(NamedTuple):
    last_seen: int
    messages: List[Dict[str, Any]]


def parse(html: str, **kwargs) -> Dict[str, Any]:
    # Get the timestamp we should send to the server next time we make a request.
    last_seen_matcher = last_seen_pattern.search(html)
    last_seen = int(last_seen_matcher.group(1))

    html = html[: html.find("<!--lastseen")]
    return Response(last_seen, ChatUtils.parseIncomingChatMessage(html))


def chat_messages_get(session: "pykollib.Session", since: int = 0) -> Coroutine[Any, Any, ClientResponse]:
    params = {"lasttime": since}
    return session.request("newchatmessages.php", params=params, parse=parse)
