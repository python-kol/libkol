from enum import Enum

import libkol

from ..Error import ItemNotFoundError, WrongKindOfItemError
from ..Item import Item
from .request import Request


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


class equip(Request):
    """
    Equips items from the inventory passed by itemId.  If a slot is specified, it will attempt to equip accessories into that slot.
    """

    def __init__(self, session: "libkol.Session", item: Item, slot: Slot) -> None:
        super().__init__(session)

        params = {"action": "equip", "which": 2, "whichitem": item.id}
        data = {"slot": slot}
        self.request = session.request(
            "inv_equip.php", pwd=True, params=params, data=data
        )

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        "Checks for errors due to equipping items you don't have, or equipping items that aren't equippable."

        if "You don't have the item you're trying to equip." in content:
            raise ItemNotFoundError("That item is not in your inventory.")

        if (
            "That's not something you can equip.  And stop screwing with the URLs."
            in content
        ):
            raise WrongKindOfItemError("That is not an equippable item.")

        return True
