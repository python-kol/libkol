import libkol

from .request import Request


class clan_stash_item_remove(Request):
    """
    Take items from the player's clan stash.
    """

    def __init__(
        self, session: "libkol.Session", item_id: int = 0, quantity: int = 0
    ) -> None:
        super().__init__(session)

        params = {"action": "takegoodies", "whichitem": item_id, "quantity": quantity}
        self.request = session.request("clan_stash.php", params=params)
