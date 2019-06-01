import pykollib

from ..Error import ItemNotFoundError, UserIsDrunkError, WrongKindOfItemError
from ..Item import Item
from ..util import parsing
from .request import Request


class eat(Request):
    """
    This request is for eating food from the inventory.

    :param session: Active session
    :param item: Consumable to eat
    """
    def __init__(self, session: "pykollib.Session", item: Item) -> None:
        super().__init__(session)

        params = {"which": 1, "whichitem": item.id}
        self.request = session.request(
            "inv_eat.php", ajax=True, pwd=True, params=params
        )

    @staticmethod
    def parser(html: str, **kwargs) -> parsing.ResourceGain:
        if "You're way too drunk already." in html:
            raise UserIsDrunkError("You're too full to eat that.")

        if "That's not booze." in html:
            raise WrongKindOfItemError("That's not something you can eat.")

        if ">You don't have the item you're trying to use.<" in html:
            raise ItemNotFoundError("Item not in inventory.")

        # Check the results
        return parsing.resource_gain(html)
