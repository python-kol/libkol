import libkol

from .request import Request


class item_discard(Request):
    def __init__(self, session: "libkol.Session", item: "libkol.Item") -> None:
        params = {"action": "discard", "whichitem": item.id}
        self.request = session.request("inventory.php", params=params)
