from typing import List

import libkol

from .request import Request
from ..util import parsing
from ..Error import UnknownError


class guild_malus(Request):
    def __init__(
        self, session: "libkol.Session", item: "libkol.Item", quantity: int = 1
    ):
        super().__init__(session)
        data = {"action": "malussmash", "whichitem": item.id, "quantity": quantity}

        self.request = session.request("guild.php", pwd=True, data=data)

    @staticmethod
    async def parser(content: str, **kwargs) -> List["libkol.types.ItemQuantity"]:
        items = await parsing.item(content)

        if len(items) == 0:
            raise UnknownError("Unknonw error using Malus")

        return items
