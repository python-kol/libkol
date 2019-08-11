from typing import List, NamedTuple

import libkol

from ..Error import (
    InvalidLocationError,
    NotEnoughMeatError,
    UnknownError,
    WrongKindOfItemError,
)
from ..util import parsing
from .request import Request
from ..Store import Store


class npc_buy(Request[parsing.ResourceGain]):
    """
    Purchases items from an NPC store.

    :param session: Active session
    :param store: NPC store to buy from
    :param item: Item to buy
    :param quantity: Quantity of said item to buy
    """

    def __init__(
        self,
        session: "libkol.Session",
        store: Store,
        item: "libkol.Item",
        quantity: int = 1,
    ) -> None:
        super().__init__(session)

        if item.store_id != store.id:
            raise WrongKindOfItemError("This item cannot be purchased in that store")

        # Gift shop is handled differently
        if store.slug == "town_giftshop.php":
            params = {"action": "buy", "howmany": quantity, "whichitem": item.id}
            self.request = session.request("town_giftshop.php", pwd=True, params=params)
            return

        if ".php" in store.slug:
            raise UnknownError("This is a special shop but we don't know how to use it")

        params = {"whichshop": store.slug, "action": "buyitem", "quantity": quantity}

        if item.store_row:
            params["whichrow"] = item.store_row
        else:
            params["whichitem"] = item.id

        self.request = session.request("shop.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> parsing.ResourceGain:
        session = kwargs["session"] # type: libkol.Session
        if len(content) == 0:
            raise InvalidLocationError("You cannot visit that store yet.")

        if "You've been sent back here by some kind of bug" in content:
            raise InvalidLocationError("The store you tried to visit doesn't exist.")

        if (
            "This store doesn't sell that item" in content
            or "Invalid item selected" in content
            or "<td>That isn't a thing that's sold here.</td>" in content
        ):
            raise WrongKindOfItemError("This store doesn't carry that item.")

        if "You can't afford " in content:
            raise NotEnoughMeatError(
                "You do not have enough meat to purchase the item(s)."
            )

        return await parsing.resource_gain(content, session)
