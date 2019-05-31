

from .request import Request

import pykollib


class clan_stash_item_remove(Request):
    def __init__(self, session: "pykollib.Session", item_id: int = 0, quantity: int = 0) -> None:
        """
        Take items from the player's clan stash.
        """
        super().__init__(session)

        params = {"action": "takegoodies", "whichitem": item_id, "quantity": quantity}
        self.request = session.request("clan_stash.php", params=params)
