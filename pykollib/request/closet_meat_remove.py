

from .request import Request

import pykollib


class closet_meat_remove(Request):
    def __init__(self, session: "pykollib.Session", amount: int = 0) -> None:
        """
        Takes meat from the player's closet.
        """
        super().__init__(session)

        params = {"action": "takemeat", "amt": amount}
        self.request = session.request("closet.php", params=params)
