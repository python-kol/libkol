from bs4 import BeautifulSoup
from yarl import URL

import libkol

from ..Error import ItemNotFoundError, WrongKindOfItemError, RequirementError
from .request import Request


class equip(Request):
    """
    Equips items from the inventory passed by itemId.  If a slot is specified, it will attempt to equip accessories into that slot.
    """

    def __init__(
        self, session: "libkol.Session", item: "libkol.Item", slot: "libkol.Slot"
    ) -> None:
        super().__init__(session)

        params = {"action": "equip", "which": 2, "whichitem": item.id}
        data = {"slot": slot}

        self.request = session.request(
            "inv_equip.php", pwd=True, params=params, data=data
        )

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        "Checks for errors due to equipping items you don't have, or equipping items that aren't equippable."
        from libkol import Item, Slot

        if "You don't have the item you're trying to equip." in content:
            raise ItemNotFoundError("That item is not in your inventory.")

        if (
            "That's not something you can equip.  And stop screwing with the URLs."
            in content
        ):
            raise WrongKindOfItemError("That is not an equippable item.")

        if "You must have at least" in content:
            raise RequirementError("Inadequate stats or level")

        soup = BeautifulSoup(content, "html.parser")
        session = kwargs["session"]  # type: libkol.Session
        url = kwargs["url"]  # type: URL

        items = soup.find_all("img", class_="hand")

        first_onclick = items[0]["onclick"]

        first = await Item[int(first_onclick[9 : first_onclick.find(",")])]

        if len(items) == 1:
            equipped = first
        else:
            unequipped = first
            equipped_onclick = items[0]["onclick"]
            equipped = await Item[int(equipped_onclick[9 : equipped_onclick.find(",")])]

        if unequipped:
            session.state["inventory"][unequipped] += 1

        query_slot = url.query.get("slot")
        slot = Slot.acc(int(query_slot)) if query_slot is not None else equipped.slot
        session.state["equipment"][slot] = equipped

        return True
