import pykollib

from ..Error import NotEnoughItemsError, WrongKindOfItemError
from ..Item import Item
from ..util import parsing
from .request import Request


class item_multi_use(Request):
    """
    Uses multiple items at once
    """
    def __init__(self, session: "pykollib.Session", item: Item, quantity: int) -> None:
        super().__init__(session)

        params = {"action": "useitem", "whichitem": item.id, "quantity": quantity}
        self.request = session.request("multiuse.php", pwd=True, params=params)

    @staticmethod
    async def parser(html: str, **kwargs) -> parsing.ResourceGain:
        if (
            "<table><tr><td>You don't have that many of that item.</td></tr></table>"
            in html
        ):
            raise NotEnoughItemsError("You don't have that many of that item.")

        if (
            "<table><tr><td>That item isn't usable in quantity.</td></tr></table>"
            in html
        ):
            raise WrongKindOfItemError("You cannot multi-use that item.")

        # Find out what happened
        return parsing.resource_gain(html)
