from aiohttp import ClientResponse
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..Session import Session


def parse(html: str, **kwargs) -> bool:
    return "<td>Whitelist updated.</td>" in html


def clanWhitelistRemovePlayerRequest(
    session: "Session", user: Union[int, str]
) -> ClientResponse:
    payload = {"action": "updatewl", "who": user, "remove": "Remove"}

    return session.request("clan_whitelist.php", data=payload, pwd=True, parse=parse)
