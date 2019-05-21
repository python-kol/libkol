from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Error import InvalidLocationError


def parse(html: str, **kwargs) -> None:
    if len(html) == 0:
        raise InvalidLocationError("You cannot use the Mind Control Device yet.")


def canadia_mindcontrol(session: "Session", level: int) -> ClientResponse:
    params = {"action": "changedial", "whichlevel": level}
    return session.request("canadia.php", params=params, parse=parse)
