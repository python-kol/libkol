import libkol

from .request import Request


class campground_rest(Request):
    """
    Rests at the player's campground.

    :param session: Active session
    """

    def __init__(self, session: "libkol.Session"):
        params = {"action": "rest"}
        self.request = session.request("campground.php", params=params)
