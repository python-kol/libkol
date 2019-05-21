from aiohttp import ClientResponse
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..pattern import PatternManager
from ..Error import InvalidLocationError, NotEnoughAdventuresError, RequestGenericError
from ..util import parsing
from ..Stat import Stat


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


def canadia_gym(session: "Session", turns: int) -> ClientResponse:
    params = {"action": "institute", "numturns": turns}
    return session.request("canadia.php", params=params, parse=parse)
