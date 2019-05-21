from aiohttp import ClientResponse
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import ItemQuantity
from ..pattern import PatternManager
from ..Error import NotEnoughMeatError, NotEnoughItemsError, RequestGenericError


def parse(html: str, **kwargs) -> bool:
    noMeatPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughMeat")
    if noMeatPattern.search(html):
        raise NotEnoughMeatError("You don't have as much meat as you're promising.")

    noItemsPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughItems")
    if noItemsPattern.search(html):
        raise NotEnoughItemsError("You don't have as many items as you're promising.")

    # Not testing for an offer being cancelled due to a bug in KoL - space reserved

    successPattern = PatternManager.getOrCompilePattern("tradeResponseSentSuccessfully")
    if successPattern.search(html) is None:
        raise RequestGenericError("Unknown error sending response to trade")

    return True


def trade_respond(
    session: "Session",
    trade_id: int,
    item_quantities: List[ItemQuantity] = [],
    meat: int = 0,
    message: str = "",
) -> ClientResponse:
    params = {
        "action": "counter",
        "whichoffer": trade_id,
        "offermeat": meat,
        "memo2": message,
    }

    for i, iq in item_quantities.enumerate():
        params["howmany{}".format(i)] = iq.quantity
        params["whichitem{}".format(i)] = iq.item.id

    return session.request("makeoffer.php", pwd=True, params=params, parse=parse)
