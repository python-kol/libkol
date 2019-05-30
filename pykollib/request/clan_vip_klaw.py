from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib

from ..Item import Item
from ..util import parsing


def parse(html: str, **kwargs) -> List[Item]:
    return parsing.item(html)


def clan_vip_klaw(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    """
    Uses the Deluxe Mr. Klaw in the clan VIP room.
    """

    params = {"action": "klaw"}
    return session.request("clan_viplounge.php", params, parse=parse)
