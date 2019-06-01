from typing import Dict, NamedTuple

import pykollib

from ..Error import InvalidLocationError, NotEnoughAdventuresError, RequestGenericError
from ..pattern import PatternManager
from ..Stat import Stat
from ..util import parsing
from .request import Request


class Response(NamedTuple):
    substats: Dict[str, int]
    stats: Dict[str, int]
    level: int


no_adventures_pattern = PatternManager.getOrCompilePattern("noAdvInstitue")
invalid_turns_pattern = PatternManager.getOrCompilePattern("invalidAdvInstitute")


class canadia_gym(Request):
    def __init__(self, session: "pykollib.Session", turns: int):
        params = {"action": "institute", "numturns": turns}
        self.request = session.request("canadia.php", params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> Response:
        if len(html) == 0:
            raise InvalidLocationError(
                "You cannot attend The Institute for Canadian Studies"
            )

        if no_adventures_pattern.search(html):
            raise NotEnoughAdventuresError(
                "You don't have enough adventures to study at the institute."
            )
        if invalid_turns_pattern.search(html):
            raise RequestGenericError(
                "That is an invalid number of turns for studying."
            )

        return Response(
            substats=parsing.substat(html, stat=Stat.Mysticality),
            stats=parsing.stat(html, stat=Stat.Mysticality),
            level=parsing.level(html),
        )
