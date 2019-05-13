from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def meatOrchidRequest(session: "Session") -> ClientResponse:
    "Uses the hanging meat orchid in the clan rumpus room."

    params = {"action": "click", "spot": 1, "furni": 4}
    return session.request("clan_rumpus.php", params=params)
