from typing import List

import libkol
from libkol import types

from .request import Request


class clan_stash_item_add(Request):
    """
    Adds items to the clan's stash.
    """

    def __init__(
        self, session: "libkol.Session", items: List[types.ItemQuantity]
    ) -> None:
        params = {"action": "addgoodies"}

        for i, iq in enumerate(items):
            params["item{}".format(i)] = str(iq.item.id)
            params["qty{}".format(i)] = str(iq.quantity)

        self.request = session.request("clan_stash.php", pwd=True)
