from typing import List

import pykollib
from .request import Request
from ..util import parsing
from ..types import ItemQuantity
from ..Error import UnknownError
from ..Item import Item

class guild_malus(Request):
    def __init__(self, session: "pykollib.Session", item: Item, quantity: int = 1):
        super().__init__(session)
        data = {"action": "malussmash", "whichitem": item.id, "quantity": quantity}

        self.request = session.request("guild.php", pwd=True, data=data)

    @staticmethod
    async def parser(html: str, **kwargs) -> List[ItemQuantity]:
        items = await parsing.item(html)

        if len(items) == 0:
            raise UnknownError("Unknonw error using Malus")

        return items
