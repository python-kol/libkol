from aiohttp import ClientResponse
from bs4 import BeautifulSoup, Tag
from typing import TYPE_CHECKING, Dict, Optional, Coroutine, Any

if TYPE_CHECKING:
    from ..Session import Session

from .equip import Slot
from ..Item import Item


def slot_to_item(soup: Tag, link: str, index: int = 0) -> Optional[Item]:
    slot_title = soup.find_all("a", href="#{}".format(link))

    if len(slot_title) == 0:
        return None

    descid = slot_title[index].parent.next_sibling.img["rel"]
    return Item.get_or_none(desc_id=descid)


def parse(html: str, **kwargs) -> Dict[Slot, Optional[Item]]:
    soup = BeautifulSoup(html, "html.parser")
    current = soup.find(id="curequip")

    return {
        Slot.Hat: slot_to_item(current, "Hats"),
        Slot.Back: slot_to_item(current, "Back"),
        Slot.Shirt: slot_to_item(current, "Shirts"),
        Slot.Weapon: slot_to_item(current, "Weapons"),
        Slot.Offhand: slot_to_item(current, "Off-Hand"),
        Slot.Pants: slot_to_item(current, "Pants"),
        Slot.Acc1: slot_to_item(current, "Accessories", 0),
        Slot.Acc2: slot_to_item(current, "Accessories", 1),
        Slot.Acc3: slot_to_item(current, "Accessories", 2),
        Slot.Familiar: slot_to_item(current, "Familiar"),
    }


def equipment(session: "Session") -> Coroutine[Any, Any, ClientResponse]:
    """
    Gets info on all equipment currently equipped.
    Returns a lookup from the item database for each item equipped.
    For accessories, two possibilities are present.  If equipping each slot seperately is enabled, each item's dictionary will contain an attribute "slot" with the number of the slot it occupies.  Otherwise, the "slot" attribute will have the value 0 for all equipped accessories.
    """
    params = {"which": 2}
    return session.request("inventory.php", params=params, parse=parse)
