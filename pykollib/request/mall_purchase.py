from dataclasses import dataclass
from typing import List

import pykollib
from .request import Request
from ..util import parsing
from ..Item import Item
from ..types import ItemQuantity
from ..Error import NotEnoughMeatError, ItemNotFoundError, UserIsIgnoringError, LimitReachedError

@dataclass
class Response:
    items: List[ItemQuantity]
    meat_gained: int

class mall_purchase(Request):
    """
    Purchases an item from the specified store. This will fail if the price per item is not given
    correctly or if the quantity is higher than the remaining quantity per day. It will purchase
    as many as possible if the quantity is higher than the number in the store.
    """

    def __init__(self, session: "pykollib.Session", store_id: int, item: Item, price: int, quantity: int = 1):
        super().__init__(session)
        data = {"buying": 1, "whichitem": "{}{:09d}".format(item.id, price), "whichstore": store_id, "quantity": quantity}

        self.request = session.request("mallstore.php", pwd=True, ajax=True, data=data)

    @staticmethod
    async def parser(content: str, **kwargs):
        if "<td>You can't afford that item.</td>" in content:
            raise NotEnoughMeatError("You cannot afford to buy this item.")

        if "<td>This store doesn't have that item at that price." in content:
            raise ItemNotFoundError("That item is not sold at that price")

        if "<td>That player will not sell to you, because you are on his or her ignore list.</td>" in content:
            raise UserIsIgnoringError("The owner of that store is ignoring you")

        if "<td>You may only buy " in content:
            raise LimitReachedError("You have hit the daily limit for this item at this store")

        items = await parsing.item(content)
        meat_gained = parsing.meat(content)

        return Response(items=items, meat_gained=meat_gained)
