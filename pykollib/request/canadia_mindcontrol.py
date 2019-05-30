from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from ..Error import InvalidLocationError


def parse(html: str, **kwargs) -> None:
    if len(html) == 0:
        raise InvalidLocationError("You cannot use the Mind Control Device yet.")


def canadia_mindcontrol(session: "pykollib.Session", level: int) -> Coroutine[Any, Any, ClientResponse]:
    params = {"action": "changedial", "whichlevel": level}
    return session.request("canadia.php", params=params, parse=parse)
