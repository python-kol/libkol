

from .request import Request

import pykollib

from ..Item import Item


class item_use(Request):
    def __init__(self, session: "pykollib.Session", item: Item) -> None:
        """
        Uses the requested item.
        """
        super().__init__(session)

        params = {"whichitem": item.id}
        self.request = session.request("inv_use.php", params=params)
