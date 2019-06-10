from dataclasses import dataclass

import libkol
from .request import Request
from ..util import parsing
from ..Item import Item
from ..types import Listing
from ..Error import (
    NotEnoughMeatError,
    ItemNotFoundError,
    UserIsIgnoringError,
    LimitReachedError,
    UnknownError,
)


@dataclass
class Response:
    item: Item
    quantity: int
    meat_gained: int


class mall_purchase(Request[Response]):
    """
    Purchases an item from the specified store. This will fail if the price per item is not given
    correctly or if the quantity is higher than the remaining quantity per day. It will purchase
    as many as possible if the quantity is higher than the number in the store.
    """

    def __init__(
        self,
        session: "libkol.Session",
        listing: Listing = None,
        store_id: int = None,
        item: Item = None,
        price: int = None,
        quantity: int = None,
    ):
        super().__init__(session)
        if listing is not None:
            store_id = listing.store_id
            item = listing.item
            price = listing.price
            quantity = (
                listing.stock
                if listing.limit == 0
                else min(listing.stock, listing.limit)
            )
        else:
            quantity = quantity or 1

        if store_id is None or item is None or price is None:
            raise TypeError(
                "You must either specify a Listing or a store_id, item and price"
            )

        params = {
            "buying": 1,
            "whichitem": "{}{:09d}".format(item.id, price),
            "whichstore": store_id,
            "quantity": quantity,
        }

        self.request = session.request(
            "mallstore.php", pwd=True, ajax=True, params=params
        )

    @staticmethod
    async def parser(content: str, **kwargs):
        if "<td>You can't afford that item.</td>" in content:
            raise NotEnoughMeatError("You cannot afford to buy this item.")

        if "<td>This store doesn't have that item at that price." in content:
            raise ItemNotFoundError("That item is not sold at that price")

        if (
            "<td>That player will not sell to you, because you are on his or her ignore list.</td>"
            in content
        ):
            raise UserIsIgnoringError("The owner of that store is ignoring you")

        if "<td>You may only buy " in content:
            raise LimitReachedError(
                "You have hit the daily limit for this item at this store"
            )

        if "<td>That doesn't make any sense.</td>" in content:
            raise TypeError("Request malformed")

        items = await parsing.item(content)

        if len(items) == 0:
            raise UnknownError("Purchase failed for unknown reason")

        if len(items) > 1:
            raise UnknownError(
                "Managed to purchase two types of item from one mall request"
            )

        meat_gained = parsing.meat(content)

        return Response(
            item=items[0].item, quantity=items[0].quantity, meat_gained=meat_gained
        )
