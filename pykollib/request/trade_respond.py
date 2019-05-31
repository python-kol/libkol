from typing import List

from .request import Request

import pykollib

from ..Error import (NotEnoughItemsError, NotEnoughMeatError,
                     UnknownError)
from ..Item import ItemQuantity
from ..pattern import PatternManager


class trade_respond(Request):
    def __init__(
        self,
        session: "pykollib.Session",
        trade_id: int,
        item_quantities: List[ItemQuantity] = [],
        meat: int = 0,
        message: str = "",
    ) -> None:
        params = {
            "action": "counter",
            "whichoffer": trade_id,
            "offermeat": meat,
            "memo2": message,
        }

        for i, iq in enumerate(item_quantities):
            params["howmany{}".format(i)] = iq.quantity
            params["whichitem{}".format(i)] = iq.item.id

        self.request = session.request("makeoffer.php", pwd=True, params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> bool:
        noMeatPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughMeat")
        if noMeatPattern.search(html):
            raise NotEnoughMeatError("You don't have as much meat as you're promising.")

        noItemsPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughItems")
        if noItemsPattern.search(html):
            raise NotEnoughItemsError("You don't have as many items as you're promising.")

        # Not testing for an offer being cancelled due to a bug in KoL - space reserved

        successPattern = PatternManager.getOrCompilePattern("tradeResponseSentSuccessfully")
        if successPattern.search(html) is None:
            raise UnknownError("Unknown error sending response to trade")

        return True
