import libkol

from .request import Request


class clan_stash_meat_add(Request):
    """
    Adds meat to the player's clan stash.
    """

    def __init__(self, session: "libkol.Session", quantity: int) -> None:
        super().__init__(session)

        params = {"action": "contribute", "howmuch": quantity}
        self.request = session.request("clan_stash.php", pwd=True, params=params)
