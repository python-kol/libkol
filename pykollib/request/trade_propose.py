from typing import List

from .request import Request

import pykollib

from ..Error import (BannedFromChatError, NotEnoughItemsError,
                     NotEnoughMeatError, RequestGenericError,
                     UserInHardcoreRoninError, UserIsIgnoringError)
from ..Item import ItemQuantity
from ..pattern import PatternManager


class trade_propose(Request):
    def __init__(
        self,
        session: "pykollib.Session",
        user_id: int,
        item_quantities: List[ItemQuantity] = [],
        meat: int = 0,
        message: str = "",
    ) -> None:
        params = {
            "action": "proposeoffer",
            "towho": user_id,
            "offermeat": meat,
            "memo": message,
        }

        for i, iq in enumerate(item_quantities):
            params["howmany{}".format(i)] = iq.quantity
            params["whichitem{}".format(i)] = iq.item.id

        self.request = session.request("makeoffer.php", pwd=True, params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> bool:
        ignorePattern = PatternManager.getOrCompilePattern("traderIgnoringUs")
        if ignorePattern.search(html):
            raise UserIsIgnoringError("That player has you on his/her ignore list.")

        roninPattern = PatternManager.getOrCompilePattern("traderIsInRoninHC")
        if roninPattern.search(html):
            raise UserInHardcoreRoninError(
                "That player is in Ronin or HC and cannot receive trade offers."
            )

        itemsPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughItems")
        if itemsPattern.search(html):
            raise NotEnoughItemsError(
                "You don't have enough of one or more of the items you're trying to trade."
            )

        meatPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughMeat")
        if meatPattern.search(html):
            raise NotEnoughMeatError(
                "You don't have as much meat as you're trying to trade."
            )

        chatBannedPattern = PatternManager.getOrCompilePattern("traderBannedFromChat")
        if chatBannedPattern.search(html):
            raise BannedFromChatError(
                "You are banned from chat and consequently cannot trade."
            )

        successPattern = PatternManager.getOrCompilePattern("tradeSentSuccessfully")
        if successPattern.search(html) is None:
            raise RequestGenericError("Unknown error sending trade offer.")

        return True
