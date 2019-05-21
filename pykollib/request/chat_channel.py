import re
from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

current_channel_pattern = re.compile(
    '<font color="?#?\w+"?>Currently in channel: ([^<>]+)<'
)


def parse(html: str, **kwargs) -> str:
    match = current_channel_pattern.search(html)
    return match.group(1)


def chat_channel(session: "Session") -> ClientResponse:
    return session.request("lchat.php", parse=parse)
