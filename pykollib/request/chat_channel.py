import re
from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

current_channel_pattern = re.compile(
    '<font color="?#?\w+"?>Currently in channel: ([^<>]+)<'
)


def parse(html: str, **kwargs) -> str:
    match = current_channel_pattern.search(html)
    return match.group(1)


def chat_channel(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    return session.request("lchat.php", parse=parse)
