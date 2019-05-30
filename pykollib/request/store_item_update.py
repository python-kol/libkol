import time
from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib
from pykollib.pattern import PatternManager

from .store_inventory import Listing

price_not_updated_pattern = PatternManager.getOrCompilePattern("mallPriceNotUpdated")


def parse(html: str, **kwargs) -> bool:
    return price_not_updated_pattern.search(html) is not None


def store_item_update(session: "pykollib.Session", listings: List[Listing]) -> Coroutine[Any, Any, ClientResponse]:
    params = {"action": "updateinv", "ajax": 1, "_": int(time.time() * 1000)}

    for listing in listings:
        params["price[{}]".format(listing.item.id)] = listing.price
        params["limit[{}]".format(listing.item.id)] = listing.limit

    return session.request("backoffice", pwd=True, params=params, parse=parse)
