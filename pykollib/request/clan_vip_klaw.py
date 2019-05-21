from aiohttp import ClientResponse
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import Item
from ..util import parsing


def parse(html: str, **kwargs) -> List[Item]:
    return parsing.item(html)


def clan_vip_klaw(session: "Session") -> ClientResponse:
    """
    Uses the Deluxe Mr. Klaw in the clan VIP room.
    """

    params = {"action": "klaw"}
    return session.request("clan_viplounge.php", params, parse=parse)
