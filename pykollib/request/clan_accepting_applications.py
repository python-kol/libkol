from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from ..Error import UnknownError
from ..util import parsing


def parse(html: str, **kwargs) -> bool:
    results = parsing.panel(html)

    if results.string == "Applications turned on.":
        return True

    if results.string == "Applications turned off.":
        return False

    raise UnknownError("Unknown response")


def clan_accepting_applications(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    "Toggle whether or not the clan accepts new applications."

    params = {"action": "noapp"}
    return session.request("clan_admin.php", params=params, parse=parse)
