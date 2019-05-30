from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib

from ..Item import ItemQuantity
from ..util import parsing


def parse(html: str, **kwargs) -> List[ItemQuantity]:
    return parsing.item(html)


def clan_vip_lookingglass(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    "Uses the Looking Glass in the clan VIP room."

    params = {"action": "lookingglass"}
    return session.request("clan_viplounge.php", params=params, parse=parse)
