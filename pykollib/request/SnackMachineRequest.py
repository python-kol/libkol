from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def snackMachineRequest(session: "Session") -> ClientResponse:
    "Uses the snack machine in the clan rumpus room."

    params = {"action": "click", "spot": 9, "furni": 2}
    return session.request("clan_rumpus.php", params=params)
