from typing import List

import libkol

from ..Error import (
    BannedFromChatError,
    NotEnoughItemsError,
    NotEnoughMeatError,
    RequestGenericError,
    UserInHardcoreRoninError,
    UserIsIgnoringError,
)
from ..types import ItemQuantity
from ..pattern import PatternManager
from .request import Request


class trade_propose(Request[bool]):
    def __init__(
        self,
        session: "libkol.Session",
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
    async def parser(content: str, **kwargs) -> bool:
        ignorePattern = PatternManager.getOrCompilePattern("traderIgnoringUs")
        if ignorePattern.search(content):
            raise UserIsIgnoringError("That player has you on his/her ignore list.")

        roninPattern = PatternManager.getOrCompilePattern("traderIsInRoninHC")
        if roninPattern.search(content):
            raise UserInHardcoreRoninError(
                "That player is in Ronin or HC and cannot receive trade offers."
            )

        itemsPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughItems")
        if itemsPattern.search(content):
            raise NotEnoughItemsError(
                "You don't have enough of one or more of the items you're trying to trade."
            )

        meatPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughMeat")
        if meatPattern.search(content):
            raise NotEnoughMeatError(
                "You don't have as much meat as you're trying to trade."
            )

        chatBannedPattern = PatternManager.getOrCompilePattern("traderBannedFromChat")
        if chatBannedPattern.search(content):
            raise BannedFromChatError(
                "You are banned from chat and consequently cannot trade."
            )

        successPattern = PatternManager.getOrCompilePattern("tradeSentSuccessfully")
        if successPattern.search(content) is None:
            raise RequestGenericError("Unknown error sending trade offer.")

        return True
