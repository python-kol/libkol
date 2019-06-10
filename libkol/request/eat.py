import libkol

from ..Error import ItemNotFoundError, UserIsDrunkError, WrongKindOfItemError
from ..Item import Item
from ..util import parsing
from .request import Request


class eat(Request[parsing.ResourceGain]):
    """
    This request is for eating food from the inventory.

    :param session: Active session
    :param item: Consumable to eat
    """

    def __init__(self, session: "libkol.Session", item: Item) -> None:
        super().__init__(session)

        params = {"which": 1, "whichitem": item.id}
        self.request = session.request(
            "inv_eat.php", ajax=True, pwd=True, params=params
        )

    @staticmethod
    async def parser(content: str, **kwargs) -> parsing.ResourceGain:
        if "You're way too drunk already." in content:
            raise UserIsDrunkError("You're too full to eat that.")

        if "That's not booze." in content:
            raise WrongKindOfItemError("That's not something you can eat.")

        if ">You don't have the item you're trying to use.<" in content:
            raise ItemNotFoundError("Item not in inventory.")

        # Check the results
        return parsing.resource_gain(content)
