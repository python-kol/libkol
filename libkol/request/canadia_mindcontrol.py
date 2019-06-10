import libkol

from ..Error import InvalidLocationError
from .request import Request


class canadia_mindcontrol(Request[bool]):
    def __init__(self, session: "libkol.Session", level: int) -> None:
        params = {"action": "changedial", "whichlevel": level}
        self.request = session.request("canadia.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        if len(content) == 0:
            raise InvalidLocationError("You cannot use the Mind Control Device yet.")

        return True
