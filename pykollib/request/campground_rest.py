import pykollib

from .request import Request


class campground_rest(Request):
    def __init__(self, session: "pykollib.Session"):
        """
        Rests at the player's campground.

        :param session: Active session
        """

        params = {"action": "rest"}
        self.request = session.request("campground.php", params=params)
