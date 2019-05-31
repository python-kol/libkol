

from .request import Request

import pykollib


class closet_meat_add(Request):
    def __init__(self, session: "pykollib.Session", quantity: int) -> None:
        """
        Adds meat to the player's closet.
        """
        super().__init__(session)

        params = {"action": "addmeat", "amt": quantity}
        self.request = session.request("closet.php", pwd=True, params=params)
