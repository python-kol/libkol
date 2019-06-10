import time
from typing import List

import libkol
from libkol.pattern import PatternManager

from .request import Request
from .store_inventory import Listing

price_not_updated_pattern = PatternManager.getOrCompilePattern("mallPriceNotUpdated")


class store_item_update(Request[bool]):
    def __init__(self, session: "libkol.Session", listings: List[Listing]) -> None:
        params = {"action": "updateinv", "ajax": 1, "_": int(time.time() * 1000)}

        for listing in listings:
            params["price[{}]".format(listing.item.id)] = listing.price
            params["limit[{}]".format(listing.item.id)] = listing.limit

        self.request = session.request("backoffice", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        return price_not_updated_pattern.search(content) is not None
