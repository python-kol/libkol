from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from .equip import Slot


def unequip(
    session: "pykollib.Session", slot: "Slot" = None, all: bool = False
) -> Coroutine[Any, Any, ClientResponse]:
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
