from aiohttp import ClientResponse
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..util import parsing
from ..Item import ItemQuantity


def parse(html: str, **kwargs) -> List[ItemQuantity]:
    return parsing.item(html)


def clan_vip_lookingglass(session: "Session") -> ClientResponse:
    "Uses the Looking Glass in the clan VIP room."

    params = {"action": "lookingglass"}
    return session.request("clan_viplounge.php", params=params, parse=parse)
