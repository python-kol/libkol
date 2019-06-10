import libkol

from ..Error import InvalidActionError, UnknownError
from ..Trophy import Trophy
from .request import Request


class trophy_buy(Request[bool]):
    def __init__(self, session: "libkol.Session", trophy: Trophy) -> None:
        super().__init__(session)
        data = {"action": "buytrophy", "whichtrophy": trophy.id}
        self.request = session.request("trophy.php", data=data)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        if "<td>You don't meet the requirements for that trophy.</td>" in content:
            raise InvalidActionError("Cannot get that trophy")

        if "<td>Your trophy has been installed at your campsite.</td>" not in content:
            raise UnknownError("Unknown error buying trophy")

        return True
