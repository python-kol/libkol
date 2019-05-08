from aiohttp import ClientResponse
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


class Slot(Enum):
    Hat = "hat"
    Weapon = "weapon"
    Offhand = "offhand"
    Shirt = "shirt"
    Pants = "pants"
    Slot1 = "acc1"
    Slot2 = "acc2"
    Slot3 = "acc3"
    Familiar = "familiarequip"


async def unequipRequest(session: "Session", slot: "Slot" = None) -> ClientResponse:
    """
    Unequips the equipment in the designated slot.

    :param slot: Will remove item from the specified Slot, or everything if Slot is None
    """

    params = {}

    if slot is None:
        params["action"] = "unequipall"
    else:
        params["action"] = "unequip"
        params["type"] = slot

    return await session.post("inv_equip.php", params=params)
