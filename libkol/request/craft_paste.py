from typing import List

import libkol
from ..Error import WrongKindOfItemError, NotEnoughMeatError, UnknownError
from .request import Request
from ..util import parsing
from ..Item import Item
from ..types import ItemQuantity


class craft_paste(Request[List[ItemQuantity]]):
    """
    Creates meat paste, meat stacks, or dense meat stacks.
    """

    def __init__(self, session: "libkol.Session", item: Item, quantity: int = 1):
        super().__init__(session)

        if item.id not in [25, 88, 258]:
            raise WrongKindOfItemError(
                "You can only create meat paste and stacks this way"
            )

        data = {"action": "makepaste", "whichitem": item.id, "qty": quantity}
        self.request = session.request("craft.php", pwd=True, data=data)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[ItemQuantity]:
        if "<td>You don't have enough Meat to make that many.</td>" in content:
            raise NotEnoughMeatError(
                "Unable to make the requested item. You don't have enough meat."
            )

        # Get the item(s) we received.
        items = await parsing.item(content)

        if len(items) == 0:
            raise UnknownError("Unknown error. No items received.")

        return items
