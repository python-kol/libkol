from aiohttp import ClientResponse
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Session import Session

from pykollib.pattern import PatternManager

import time

from .store_inventory import Listing

price_not_updated_pattern = PatternManager.getOrCompilePattern("mallPriceNotUpdated")


def parse(html: str, **kwargs) -> bool:
    return price_not_updated_pattern.search(html) is not None


def store_item_update(session: "Session", listings: List[Listing]) -> ClientResponse:
    params = {"action": "updateinv", "ajax": 1, "_": int(time.time() * 1000)}

    for listing in listings:
        params["price[{}]".format(listing.item.id)] = listing.price
        params["limit[{}]".format(listing.item.id)] = listing.limit

    return session.request("backoffice", pwd=True, params=params, parse=parse)
