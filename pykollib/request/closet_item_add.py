import pykollib

from ..Item import Item
from .request import Request


class closet_item_add(Request):
    def __init__(self, session: "pykollib.Session", item: Item, quantity: int) -> None:
        """
        Adds items to the player's closet.
        """
        super().__init__(session)

        params = {
            "action": "closetpush",
            "whichitem": item.id,
            "qty": quantity,
            "ajax": 1,
        }
        self.request = session.request("fillcloset.php", pwd=True, params=params)
