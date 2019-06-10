import libkol

from ..Item import Item
from .request import Request


class closet_item_add(Request):
    """
    Adds items to the player's closet.
    """

    def __init__(self, session: "libkol.Session", item: Item, quantity: int) -> None:
        super().__init__(session)

        params = {
            "action": "closetpush",
            "whichitem": item.id,
            "qty": quantity,
            "ajax": 1,
        }
        self.request = session.request("fillcloset.php", pwd=True, params=params)
