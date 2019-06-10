from typing import List

import pykollib
from pykollib import types

from .request import Request


class clan_stash_item_add(Request):
    """
    Adds items to the clan's stash.
    """

    def __init__(
        self, session: "pykollib.Session", items: List[types.ItemQuantity]
    ) -> None:
        params = {"action": "addgoodies"}

        for i, iq in enumerate(items):
            params["item{}".format(i)] = str(iq.item.id)
            params["qty{}".format(i)] = str(iq.quantity)

        self.request = session.request("clan_stash.php", pwd=True)
