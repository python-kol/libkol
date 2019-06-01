import pykollib

from .request import Request


class adventure(Request):
    """
    A request used to initiate an adventure at any location.

    :param session: Active Session
    :param location_id: Id of the location in which to adventure
    """

    def __init__(self, session: "pykollib.Session", location_id: int):
        params = {"snarfblat": location_id}

        self.request = session.request("adventure.php", params=params)
