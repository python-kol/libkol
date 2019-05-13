from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def sodaMachineRequest(session: "Session") -> ClientResponse:
    "Uses the soda machine in the clan rumpus room."

    params = {"action": "click", "spot": 3, "furni": 1}
    return session.request("clan_rumpus.php", params=params)
