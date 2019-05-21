from aiohttp import ClientResponse
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..util import parsing
from ..Item import Item


def parse(html: str, **kwargs) -> List[Item]:
    return parsing.item(html)


def clan_vip_crimbotree(session: "Session") -> ClientResponse:
    "Uses the Crimbo Tree in the clan VIP room."

    params = {"action": "crimbotree"}
    return session.request("clan_viplounge.php", params=params, parse=parse)
