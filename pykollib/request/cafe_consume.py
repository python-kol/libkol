from .request import Request

import pykollib

from ..Error import (InvalidLocationError, NotEnoughMeatError,
                     WrongKindOfItemError)
from ..Item import Item
from ..pattern import PatternManager
from ..util import parsing
from .cafe_menu import Cafe

cannot_go_pattern = PatternManager.getOrCompilePattern("userShouldNotBeHere")


class cafe_consume(Request):
    def __init__(self, session: "pykollib.Session", cafe: Cafe, item: Item) -> None:
        """
        Purchases items from a cafe.

        :param cafe: Cafe to use
        :param item: Item to consume
        """

        params = {"action": "CONSUME!", "cafeid": cafe, "whichitem": item.id}
        self.request = session.request("cafe.php", pwd=True, params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> parsing.ResourceGain:
        if cannot_go_pattern.search(html):
            raise InvalidLocationError("You cannot reach that cafe.")
        if "This store doesn't sell that item" in html or "Invalid item selected" in html:
            raise WrongKindOfItemError("This cafe doesn't carry that item.")
        if "You can't afford " in html:
            raise NotEnoughMeatError("You do not have enough meat to purchase the item(s).")

        return parsing.resource_gain(html)
