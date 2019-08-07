import libkol

from ..Error import InvalidLocationError, NotEnoughAdventuresError, RequestGenericError
from ..pattern import PatternManager
from ..util import parsing
from .request import Request

no_adventures_pattern = PatternManager.getOrCompilePattern("noAdvInstitue")
invalid_turns_pattern = PatternManager.getOrCompilePattern("invalidAdvInstitute")


class canadia_gym(Request[parsing.ResourceGain]):
    def __init__(self, session: "libkol.Session", turns: int):
        params = {"action": "institute", "numturns": turns}
        self.request = session.request("canadia.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> parsing.ResourceGain:
        session = kwargs["session"]  # type: libkol.Session
        if len(content) == 0:
            raise InvalidLocationError(
                "You cannot attend The Institute for Canadian Studies"
            )

        if no_adventures_pattern.search(content):
            raise NotEnoughAdventuresError(
                "You don't have enough adventures to study at the institute."
            )
        if invalid_turns_pattern.search(content):
            raise RequestGenericError(
                "That is an invalid number of turns for studying."
            )

        return await parsing.resource_gain(content, session)
