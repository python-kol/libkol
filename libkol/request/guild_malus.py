from typing import List

import libkol
from .request import Request
from ..util import parsing
from ..types import ItemQuantity
from ..Error import UnknownError
from ..Item import Item


class guild_malus(Request):
    def __init__(self, session: "libkol.Session", item: Item, quantity: int = 1):
        super().__init__(session)
        data = {"action": "malussmash", "whichitem": item.id, "quantity": quantity}

        self.request = session.request("guild.php", pwd=True, data=data)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[ItemQuantity]:
        items = await parsing.item(content)

        if len(items) == 0:
            raise UnknownError("Unknonw error using Malus")

        return items
