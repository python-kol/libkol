

from .request import Request

import pykollib

from ..Item import Item


class item_discard(Request):
    def __init__(
        self,
        session: "pykollib.Session", item: Item
    ) -> None:
        params = {"action": "discard", "whichitem": item.id}
        self.request = session.request("inventory.php", params=params)
