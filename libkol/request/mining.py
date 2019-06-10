import libkol

from .request import Request
from ..Error import InvalidLocationError, InvalidOutfitError


class mining(Request[str]):
    """
    A request used to visit a mine.

    :param session: Active Session
    :param location_id: Id of the mine to visit
    """

    def __init__(self, session: "libkol.Session", mine: int):
        super().__init__(session)
        params = {"mine": mine}

        self.request = session.request("mining.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> str:
        if "<td>That's not a valid mine.</td>" in content:
            raise InvalidLocationError("Mine not found or cannot be accessed")

        if "<td>You can't mine without the proper equipment" in content:
            raise InvalidOutfitError("Modifier and outfit requirements not met")

        return content
