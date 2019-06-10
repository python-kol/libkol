import libkol

from ..Error import ItemNotFoundError, UnknownError
from ..Item import Item
from ..pattern import PatternManager
from .request import Request


class store_item_remove(Request[bool]):
    """
    Take a single item from your store using the new Mall interface from Sep 2013

    Class expects at least an itemId. If no quantity is given, a quantity of 1 is assumed

    Todo: add option to remove all of an item. This will require calling StoreInventoryRequest
    and figuring out how many of the item there are.

    :param session: Active session
    :param item: Item to remove
    :param quantity: Amount of that item to remove
    """

    def __init__(
        self, session: "libkol.Session", item: Item, quantity: int = 1
    ) -> None:
        super().__init__(session)

        params = {"action": "removeitem", "itemid": item.id, "qty": quantity}
        self.request = session.request("backoffice.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        # First parse for errors
        notEnoughPattern = PatternManager.getOrCompilePattern("dontHaveThatManyInStore")
        if notEnoughPattern.search(content):
            raise ItemNotFoundError("You either don't have that item, or not enough")

        # Check if responseText matches the success pattern. If not, raise error.
        itemTakenSuccessfully = PatternManager.getOrCompilePattern(
            "itemTakenSuccessfully"
        )
        if itemTakenSuccessfully.search(content) is None:
            raise UnknownError("Something went wrong with the taking of the item.")

        return True
