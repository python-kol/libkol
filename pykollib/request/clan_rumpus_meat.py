from enum import Enum
from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..util import parsing


def parse(html: str) -> int:
    return parsing.meat(html)


class Type(Enum):
    Bush = (4, 2)
    Tree = (9, 3)
    Orchid = (1, 4)


def clan_rumpus_meat(session: "Session", type: Type) -> ClientResponse:
    "Uses the meat bush in the clan rumpus room."

    params = {"action": "click", "spot": type.value[0], "furni": type.value[1]}
    return session.request("clan_rumpus.php", params=params, parse=parse)
