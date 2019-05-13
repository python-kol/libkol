from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def mrKlawRequest(session: "Session") -> ClientResponse:
    "Uses the Mr. Klaw in the clan rumpus room."

    params = {"action": "click", "spot": 3, "furni": 3}

    return session.request("clan_rumpus.php", params=params)
