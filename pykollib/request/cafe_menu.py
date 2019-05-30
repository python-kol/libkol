from enum import Enum
from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib

from ..Error import InvalidLocationError, RequestGenericError
from ..Item import Item
from ..pattern import PatternManager

menu_item_pattern = PatternManager.getOrCompilePattern("menuItem")
cannot_go_pattern = PatternManager.getOrCompilePattern("userShouldNotBeHere")


def parse(html: str, **kwargs) -> List[Item]:
    if cannot_go_pattern.search(html):
        raise InvalidLocationError("You cannot reach that cafe.")

    items = []
    for match in menu_item_pattern.finditer(html):
        descId = match.group(2)
        if descId.isdigit() is False:
            continue

        items += [Item.get_or_none(desc_id=int(descId))]

    if len(items) == 0:
        raise RequestGenericError("Retrieved an Empty Menu")

    return items


class Cafe(Enum):
    ChezSnootee = 1
    Microbrewery = 2
    HellsKitchen = 3


def cafe_menu(session: "pykollib.Session", cafe: Cafe) -> Coroutine[Any, Any, ClientResponse]:
    """
    Check the current menu at a cafe.

    :params session: KoL session
    :params cafe: The Cafe from which to get the menu
    """

    params = {"cafeid": cafe}
    return session.request("cafe.php", pwd=True, params=params, parse=parse)
