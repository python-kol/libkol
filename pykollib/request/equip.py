from aiohttp import ClientResponse
from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from ..Session import Session

from ..Error import ItemNotFoundError, WrongKindOfItemError
from ..Item import Item


class Slot(Enum):
    Hat = "hat"
    Back = "back"
    Weapon = "weapon"
    Offhand = "offhand"
    Shirt = "shirt"
    Pants = "pants"
    Acc1 = "acc1"
    Acc2 = "acc2"
    Acc3 = "acc3"
    Familiar = "familiarequip"


def parse(html: str, **kwargs) -> bool:
    "Checks for errors due to equipping items you don't have, or equipping items that aren't equippable."

    if "You don't have the item you're trying to equip." in html:
        raise ItemNotFoundError("That item is not in your inventory.")

    if "That's not something you can equip.  And stop screwing with the URLs." in html:
        raise WrongKindOfItemError("That is not an equippable item.")

    return True


def equip(session: "Session", item: Item, slot: Slot) -> ClientResponse:
    """
    Equips items from the inventory passed by itemId.  If a slot is specified, it will attempt to equip accessories into that slot.
    """

    params = {"action": "equip", "which": 2, "whichitem": item.id}
    data = {"slot": slot}
    return session.request(
        "inv_equip.php", pwd=True, params=params, data=data, parse=parse
    )
