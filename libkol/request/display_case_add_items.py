from typing import List

import libkol

from ..types import ItemQuantity
from .request import Request


class display_case_add_items(Request):
    """
    Adds items to the player's display case.

    :param session: Active session
    :param items: List of items and their quantities to add to the case
    """

    def __init__(self, session: "libkol.Session", items: List[ItemQuantity]) -> None:
        super().__init__(session)

        params = {"action": "put"}

        for i, iq in enumerate(items):
            params["whichitem{}".format(i)] = str(iq.item.id)
            params["howmany{}".format(i)] = str(iq.quantity)

        self.request = session.request("managecollection.php", pwd=True, params=params)
