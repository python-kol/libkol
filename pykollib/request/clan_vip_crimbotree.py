from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib

from ..Item import Item
from ..util import parsing


def parse(html: str, **kwargs) -> List[Item]:
    return parsing.item(html)


def clan_vip_crimbotree(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    "Uses the Crimbo Tree in the clan VIP room."

    params = {"action": "crimbotree"}
    return session.request("clan_viplounge.php", params=params, parse=parse)
