

from .request import Request

import pykollib


class clan_stash_meat_add(Request):
    def __init__(self, session: "pykollib.Session", quantity: int) -> None:
        """
        Adds meat to the player's clan stash.
        """
        super().__init__(session)

        params = {"action": "contribute", "howmuch": quantity}
        self.request = session.request("clan_stash.php", pwd=True, params=params)
