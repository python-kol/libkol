import libkol

from ..Error import InvalidLocationError, NotEnoughMeatError, WrongKindOfItemError
from ..Item import Item
from ..pattern import PatternManager
from ..util import parsing
from .cafe_menu import Cafe
from .request import Request

cannot_go_pattern = PatternManager.getOrCompilePattern("userShouldNotBeHere")


class cafe_consume(Request[parsing.ResourceGain]):
    """
    Purchases items from a cafe.

    :param cafe: Cafe to use
    :param item: Item to consume
    """

    def __init__(self, session: "libkol.Session", cafe: Cafe, item: Item) -> None:
        params = {"action": "CONSUME!", "cafeid": cafe, "whichitem": item.id}
        self.request = session.request("cafe.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> parsing.ResourceGain:
        if cannot_go_pattern.search(content):
            raise InvalidLocationError("You cannot reach that cafe.")
        if (
            "This store doesn't sell that item" in content
            or "Invalid item selected" in content
        ):
            raise WrongKindOfItemError("This cafe doesn't carry that item.")
        if "You can't afford " in content:
            raise NotEnoughMeatError(
                "You do not have enough meat to purchase the item(s)."
            )

        return parsing.resource_gain(content)
