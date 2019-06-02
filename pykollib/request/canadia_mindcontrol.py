import pykollib

from ..Error import InvalidLocationError
from .request import Request


class canadia_mindcontrol(Request):
    def __init__(self, session: "pykollib.Session", level: int) -> None:
        params = {"action": "changedial", "whichlevel": level}
        self.request = session.request("canadia.php", params=params)

    @staticmethod
    async def parser(html: str, **kwargs) -> None:
        if len(html) == 0:
            raise InvalidLocationError("You cannot use the Mind Control Device yet.")
