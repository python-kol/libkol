from enum import Enum
from typing import List

from .request import Request

import pykollib

from ..Error import InvalidLocationError, RequestGenericError
from ..Item import Item
from ..pattern import PatternManager

menu_item_pattern = PatternManager.getOrCompilePattern("menuItem")
cannot_go_pattern = PatternManager.getOrCompilePattern("userShouldNotBeHere")


class Cafe(Enum):
    ChezSnootee = 1
    Microbrewery = 2
    HellsKitchen = 3


class cafe_menu(Request):
    def __init__(self, session: "pykollib.Session", cafe: Cafe):
        """
        Check the current menu at a cafe.

        :params session: KoL session
        :params cafe: The Cafe from which to get the menu
        """

        params = {"cafeid": cafe}
        self.request = session.request("cafe.php", pwd=True, params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> List[Item]:
        if cannot_go_pattern.search(html):
            raise InvalidLocationError("You cannot reach that cafe.")

        items = [] # type: List[Item]
        for match in menu_item_pattern.finditer(html):
            desc_id = match.group(2)
            if desc_id.isdigit() is False:
                continue

            item = Item.get_or_none(desc_id=int(desc_id))

            if item is None:
                print("Unrecognised item with descid {}".format(desc_id))
                continue

            items += [item]

        if len(items) == 0:
            raise RequestGenericError("Retrieved an Empty Menu")

        return items
