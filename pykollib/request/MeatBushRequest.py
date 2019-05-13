from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def meatBushRequest(session: "Session") -> ClientResponse:
    "Uses the meat bush in the clan rumpus room."

    params = {"action": "click", "spot": 4, "furni": 2}
    return session.request("clan_rumpus.php", params=params)
