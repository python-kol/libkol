from typing import List, NamedTuple

import libkol

from ..Item import Item
from ..pattern import PatternManager
from .request import Request

store_inventory_pattern = PatternManager.getOrCompilePattern("storeInventory")


class Listing(NamedTuple):
    item: Item  # The item
    order: int  #  Item order in your store. 0 is the first listed and so on
    quantity: int  # The number of the item in your mall store.
    price: int  # The price of the item in your mall store.
    limit: int  # The limit on the item in your mall store.
    cheapest: int  # The cheapest in mall. This includes limited items, use at own risk.


class store_inventory(Request):
    """
    Get a list of items currently in a user's store
    """

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        params = {"which": 1}
        self.request = session.request("backoffice.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Listing]:
        """
        Searches backoffice.php for item name, quantity, price, limit, and ID.
        """
        return [
            Listing(
                item=await Item.get_or_discover(id=int(match.group(7))),
                order=int(match.group(2)),
                quantity=int(match.group(5)),
                price=int(match.group(8)),
                limit=int(match.group(10)),
                cheapest=int(match.group(12)),
            )
            for match in store_inventory_pattern.finditer(content)
        ]
