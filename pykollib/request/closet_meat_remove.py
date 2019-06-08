import pykollib

from .request import Request


class closet_meat_remove(Request):
    """
    Takes meat from the player's closet.
    """

    def __init__(self, session: "pykollib.Session", amount: int = 0) -> None:
        super().__init__(session)

        params = {"action": "takemeat", "amt": amount}
        self.request = session.request("closet.php", params=params)
