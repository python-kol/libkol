from typing import NamedTuple, Optional

from bs4 import BeautifulSoup, Tag

import libkol

from ..Item import Item
from .request import Request


class Outfit(NamedTuple):
    hat: Optional[Item]
    back: Optional[Item]
    shirt: Optional[Item]
    weapon: Optional[Item]
    offhand: Optional[Item]
    pants: Optional[Item]
    acc1: Optional[Item]
    acc2: Optional[Item]
    acc3: Optional[Item]
    familiar: Optional[Item]


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
    async def slot_to_item(soup: Tag, link: str, index: int = 0) -> Optional[Item]:
        slot_title = soup.find_all("a", href="#{}".format(link))

        if len(slot_title) == 0:
            return None

        descid = slot_title[index].parent.next_sibling.img["rel"]
        return await Item.get_or_discover(desc_id=descid)

    @classmethod
    async def parser(cls, content: str, **kwargs) -> Outfit:
        soup = BeautifulSoup(content, "html.parser")
        current = soup.find(id="curequip")

        return Outfit(
            hat=(await cls.slot_to_item(current, "Hats")),
            back=(await cls.slot_to_item(current, "Back")),
            shirt=(await cls.slot_to_item(current, "Shirts")),
            weapon=(await cls.slot_to_item(current, "Weapons")),
            offhand=(await cls.slot_to_item(current, "Off-Hand")),
            pants=(await cls.slot_to_item(current, "Pants")),
            acc1=(await cls.slot_to_item(current, "Accessories", 0)),
            acc2=(await cls.slot_to_item(current, "Accessories", 1)),
            acc3=(await cls.slot_to_item(current, "Accessories", 2)),
            familiar=(await cls.slot_to_item(current, "Familiar")),
        )
