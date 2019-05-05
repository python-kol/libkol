from aiohttp import ClientResponse
from typing import Dict, Any, TYPE_CHECKING
import re
from pykollib.util import ChatUtils

if TYPE_CHECKING:
    from ..Session import Session


lastSeenPattern = re.compile(r"lastseen:([0-9]+)")


async def parse(html: str, **kwargs) -> Dict[str, Any]:
    # Get the timestamp we should send to the server next time we make a request.
    lastSeen = lastSeenPattern.search(html).group(1)
    html = html[: html.find("<!--lastseen")]
    return {
        "lastSeen": lastSeen,
        "chatMessages": ChatUtils.parseIncomingChatMessage(html),
    }


async def getChatMessagesRequest(session: "Session", since: int = 0) -> ClientResponse:
    params = {"lasttime": since}
    return await session.post("newchatmessages.php", params=params, parse=parse)
