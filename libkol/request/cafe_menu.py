from enum import Enum
from typing import List

import libkol

from ..Error import InvalidLocationError, RequestGenericError
from ..Item import Item
from ..pattern import PatternManager
from .request import Request

menu_item_pattern = PatternManager.getOrCompilePattern("menuItem")
cannot_go_pattern = PatternManager.getOrCompilePattern("userShouldNotBeHere")


class Cafe(Enum):
    ChezSnootee = 1
    Microbrewery = 2
    HellsKitchen = 3


class cafe_menu(Request[List[Item]]):
    """
    Check the current menu at a given cafe.

    :params session: KoL session
    :params cafe: The Cafe from which to get the menu
    """

    def __init__(self, session: "libkol.Session", cafe: Cafe):
        params = {"cafeid": cafe}
        self.request = session.request("cafe.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Item]:
        if cannot_go_pattern.search(content):
            raise InvalidLocationError("You cannot reach that cafe.")

        items = []  # type: List[Item]
        for match in menu_item_pattern.finditer(content):
            desc_id = match.group(2)
            if desc_id.isdigit() is False:
                continue

            item = await Item.get_or_discover(desc_id=int(desc_id))

            if item is None:
                print("Unrecognised item with descid {}".format(desc_id))
                continue

            items += [item]

        if len(items) == 0:
            raise RequestGenericError("Retrieved an Empty Menu")

        return items
