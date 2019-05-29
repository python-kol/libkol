from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from .cafe_menu import Cafe
from ..pattern import PatternManager
from ..util import parsing
from ..Error import InvalidLocationError, WrongKindOfItemError, NotEnoughMeatError
from ..Item import Item

cannot_go_pattern = PatternManager.getOrCompilePattern("userShouldNotBeHere")


def parse(html: str, **kwargs) -> parsing.ResourceGain:
    if cannot_go_pattern.search(html):
        raise InvalidLocationError("You cannot reach that cafe.")
    if "This store doesn't sell that item" in html or "Invalid item selected" in html:
        raise WrongKindOfItemError("This cafe doesn't carry that item.")
    if "You can't afford " in html:
        raise NotEnoughMeatError("You do not have enough meat to purchase the item(s).")

    return parsing.resource_gain(html)


def cafe_consume(session: "Session", cafe: Cafe, item: Item) -> ClientResponse:
    """
    Purchases items from a cafe.

    :param cafe: Cafe to use
    :param item: Item to consume
    """

    params = {"action": "CONSUME!", "cafeid": cafe, "whichitem": item.id}
    return session.request("cafe.php", pwd=True, params=params, parse=parse)
