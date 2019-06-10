import libkol

from ..Item import Item
from .request import Request


class item_discard(Request):
    def __init__(self, session: "libkol.Session", item: Item) -> None:
        params = {"action": "discard", "whichitem": item.id}
        self.request = session.request("inventory.php", params=params)
