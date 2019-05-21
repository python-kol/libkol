from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from .equip import Slot


def unequip(
    session: "Session", slot: "Slot" = None, all: bool = False
) -> ClientResponse:
    """
    Unequips the equipment in the designated slot.

    :param slot: Will remove item from the specified Slot
    :param all: Will remove everything regardless of slot
    """

    params = {}

    if all:
        params["action"] = "unequipall"
    else:
        params["action"] = "unequip"
        params["type"] = slot

    return session.request("inv_equip.php", params=params)
