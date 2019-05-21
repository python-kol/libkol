from aiohttp import ClientResponse
from typing import NamedTuple, TYPE_CHECKING, Dict, Any, List
import re

if TYPE_CHECKING:
    from ..Session import Session

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


def chat_messages_get(session: "Session", since: int = 0) -> ClientResponse:
    params = {"lasttime": since}
    return session.request("newchatmessages.php", params=params, parse=parse)
