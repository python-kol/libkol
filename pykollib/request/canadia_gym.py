from typing import Any, Coroutine, NamedTuple

from aiohttp import ClientResponse

import pykollib

from ..Error import (InvalidLocationError, NotEnoughAdventuresError,
                     RequestGenericError)
from ..pattern import PatternManager
from ..Stat import Stat
from ..util import parsing


class Response(NamedTuple):
    substats: int
    stats: int
    level: int


no_adventures_pattern = PatternManager.getOrCompilePattern("noAdvInstitue")
invalid_turns_pattern = PatternManager.getOrCompilePattern("invalidAdvInstitute")


def parse(html: str, **kwargs) -> Response:
    if len(html) == 0:
        raise InvalidLocationError(
            "You cannot attend The Institute for Canadian Studies"
        )

    if no_adventures_pattern.search(html):
        raise NotEnoughAdventuresError(
            "You don't have enough adventures to study at the institute."
        )
    if invalid_turns_pattern.search(html):
        raise RequestGenericError("That is an invalid number of turns for studying.")

    return Response(
        {
            "substats": parsing.substat(html, stat=Stat.Mysticality),
            "stats": parsing.stat(html, stat=Stat.Mysticality),
            "level": parsing.level(html),
        }
    )


def canadia_gym(session: "pykollib.Session", turns: int) -> Coroutine[Any, Any, ClientResponse]:
    params = {"action": "institute", "numturns": turns}
    return session.request("canadia.php", params=params, parse=parse)
