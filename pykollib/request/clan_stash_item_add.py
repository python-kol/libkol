from typing import List

from .request import Request

import pykollib

from ..Item import ItemQuantity


class clan_stash_item_add(Request):
    def __init__(self, session: "pykollib.Session", items: List[ItemQuantity]) -> None:
        """
        Adds items to the clan's stash.
        """

        params = {"action": "addgoodies"}

        for i, iq in enumerate(items):
            params["item{}".format(i)] = str(iq.item.id)
            params["qty{}".format(i)] = str(iq.quantity)

        self.request = session.request("clan_stash.php", pwd=True)
