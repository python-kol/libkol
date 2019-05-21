from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Error import UnknownError
from ..util import parsing


def parse(html: str, **kwargs) -> bool:
    results = parsing.panel(html)

    if results.string == "Applications turned on.":
        return True

    if results.string == "Applications turned off.":
        return False

    raise UnknownError("Unknown response")


def clan_applications_toggle(session: "Session") -> ClientResponse:
    "Toggle whether or not the clan accepts new applications."

    params = {"action": "noapp"}
    return session.request("clan_admin.php", params=params, parse=parse)
