from typing import Dict, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag

import libkol

from .request import Request


class equipment(Request):
    """
    Gets info on all equipment currently equipped.
    Returns a lookup from the item database for each item equipped.
    For accessories, two possibilities are present.  If equipping each slot seperately is enabled, each item's dictionary will contain an attribute "slot" with the number of the slot it occupies.  Otherwise, the "slot" attribute will have the value 0 for all equipped accessories.
    """

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        params = {"which": 2}
        self.request = session.request("inventory.php", params=params)

    @staticmethod
    async def slot_to_item(
        soup: Tag, link: str, index: int = 0
    ) -> Optional["libkol.Item"]:
        from libkol import Item

        slot_title = soup.find_all("a", href=f"#{link}")

        if len(slot_title) <= index:
            return None

        desc_img = slot_title[index].parent.next_sibling.img

        if desc_img is None:
            return None

        return await Item.get_or_discover(desc_id=desc_img["rel"])

    @classmethod
    async def parser(
        cls, content: str, **kwargs
    ) -> Dict["libkol.Slot", Optional["libkol.Item"]]:
        from libkol import Slot

        session = kwargs["session"]  # type: libkol.Session

        soup = BeautifulSoup(content, "html.parser")
        current = soup.find(id="curequip")

        eq = {
            Slot.Hat: (await cls.slot_to_item(current, "Hats")),
            Slot.Back: (await cls.slot_to_item(current, "Back")),
            Slot.Shirt: (await cls.slot_to_item(current, "Shirts")),
            Slot.Weapon: (await cls.slot_to_item(current, "Weapons")),
            Slot.Offhand: (await cls.slot_to_item(current, "Off-Hand")),
            Slot.Pants: (await cls.slot_to_item(current, "Pants")),
            Slot.Acc1: (await cls.slot_to_item(current, "Accessories", 0)),
            Slot.Acc2: (await cls.slot_to_item(current, "Accessories", 1)),
            Slot.Acc3: (await cls.slot_to_item(current, "Accessories", 2)),
            Slot.FamiliarEquipment: (await cls.slot_to_item(current, "Familiar")),
        }

        session.state.equipment = eq
        return eq
