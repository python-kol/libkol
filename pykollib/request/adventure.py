import pykollib

from .request import Request


class adventure(Request):
    def __init__(self, session: "pykollib.Session", location_id: int):
        """
        A request used to initiate an adventure at any location.

        :param session: Active Session
        :param location_id: Id of the location in which to adventure
        """
        params = {"snarfblat": location_id}

        self.request = session.request("adventure.php", params=params)
