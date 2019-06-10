from typing import List

import libkol

from ..Error import ItemNotFoundError, UnknownError, WrongKindOfItemError
from ..types import ItemQuantity
from ..Item import Item
from ..util import parsing
from .request import Request


class hermit_trade(Request):
    def __init__(
        self, session: "libkol.Session", item: Item, quantity: int = 1
    ) -> None:
        data = {"action": "trade", "quantity": quantity, "whichitem": item.id}
        self.request = session.request("hermit.php", data=data)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[ItemQuantity]:
        if (
            "you are able to infer that he doesn't have enough clovers to make that trade"
            in content
        ):
            raise ItemNotFoundError(
                "The Hermit doesn't have enough clovers for that.", item=24
            )

        if "You don't have enough stuff" in content:
            raise ItemNotFoundError(
                "You don't have enough worthless items for that.", item=43
            )

        if "You don't have enough Hermit Permits to trade for that many" in content:
            raise ItemNotFoundError(
                "You don't have enough hermit permits for that.", item=42
            )

        if "The Hermit doesn't have that item" in content:
            raise WrongKindOfItemError("The Hermit doesn't have any of those.")

        if "You make a trade with the Hermit." not in content:
            raise UnknownError("Unknown error")

        return await parsing.item(content)
