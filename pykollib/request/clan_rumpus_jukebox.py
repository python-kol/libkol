from aiohttp import ClientResponse
from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from ..Session import Session

from ..util import parsing


def parse(html: str, **kwargs) -> List[Dict[str, Any]]:
    return parsing.effects(html)


def clan_rumpus_jukebox(session: "Session") -> ClientResponse:
    "Uses the jukebox in the clan rumpus room."

    params = {"action": "click", "spot": 3, "furni": 2}
    return session.request("clan_rumpus.php", params=params, parse=parse)
