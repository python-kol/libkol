from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def oldTimeyRadioRequest(session: "Session") -> ClientResponse:
    "Uses the Old-Timey Radio in the clan rumpus room."

    params = {"action": "click", "spot": 4, "furni": 1}
    return session.request("clan_rumpus.php", params=params)
