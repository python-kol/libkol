from bs4 import BeautifulSoup
from yarl import URL
from typing import List
import libkol

from .request import Request


class unequip(Request):
    """
    Unequips the equipment in the designated slot.

    :param slot: Will unequip item from the specified Slot, or completely undress if `slot` is None
    """

    def __init__(self, session: "libkol.Session", slot: "libkol.Slot" = None) -> None:
        super().__init__(session)

        params = {}

        if slot is None:
            params["action"] = "unequipall"
        else:
            params["action"] = "unequip"
            params["type"] = slot.value

        self.request = session.request("inv_equip.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List["libkol.Item"]:
        from libkol import Item, Slot

        session = kwargs["session"]  # type: libkol.Session
        url = kwargs["url"]  # type: URL

        if content == "":
            return []

        if "All items unequipped." in content:
            unequipped = session.state.equipment
        else:
            soup = BeautifulSoup(content, "html.parser")
            img = soup.find("img", class_="hand")

            item = await Item[int(img["onclick"][9:-1])]
            slot = Slot(url.query["type"])
            unequipped = {slot: item}

        for slot, item in unequipped.items():
            session.state.equipment[slot] = None
            session.state.inventory[item] += 1

        return unequipped.values()
