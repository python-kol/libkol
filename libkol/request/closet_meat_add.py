import libkol

from .request import Request


class closet_meat_add(Request):
    """
    Adds meat to the player's closet.
    """

    def __init__(self, session: "libkol.Session", quantity: int) -> None:
        super().__init__(session)

        params = {"action": "addmeat", "amt": quantity}
        self.request = session.request("closet.php", pwd=True, params=params)
