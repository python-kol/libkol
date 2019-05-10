from aiohttp import ClientResponse
from typing import Dict, Any, TYPE_CHECKING

from pykollib.pattern import PatternManager

if TYPE_CHECKING:
    from ..Session import Session

currentChannelPattern = PatternManager.getOrCompilePattern("currentChatChannel")


def parse(html: str, **kwargs) -> Dict[str, Any]:
    match = currentChannelPattern.search(html)
    return {"current_channel": match.group(1)}


def openChatRequest(session: "Session") -> ClientResponse:
    return session.request("lchat.php", parse=parse)
