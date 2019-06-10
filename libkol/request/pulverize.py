from typing import List

import libkol

from ..Error import ItemNotFoundError, WrongKindOfItemError
from ..Item import Item
from ..types import ItemQuantity
from ..util import parsing
from .request import Request


class pulverize(Request):
    def __init__(
        self, session: "libkol.Session", item: Item, quantity: int = 1
    ) -> None:
        params = {
            "action": "pulverize",
            "mode": "smith",
            "smashitem": item.id,
            "qty": quantity,
        }

        self.request = session.request("craft.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[ItemQuantity]:
        if "<td>That's not something you can pulverize.</td>" in content:
            raise WrongKindOfItemError("That item cannot be pulverized")

        if "<td>You haven't got that many" in content:
            raise ItemNotFoundError("Not enough of that item")

        return await parsing.item(content)
