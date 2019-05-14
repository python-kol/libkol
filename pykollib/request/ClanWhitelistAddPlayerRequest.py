from aiohttp import ClientResponse
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..Session import Session


def parse(html: str, **kwargs):
    success = " added to whitelist.</td>" in html
    already = "<td>That player is already on the whitelist.</td>" in html

    return {"success": success or already, "already": already}


def clanWhitelistAddPlayerRequest(
    session: "Session", user: Union[int, str], rank: int = 0, title: str = ""
) -> ClientResponse:
    payload = {"action": "add", "addwho": user, "level": rank, "title": title}

    return session.request("clan_whitelist.php", data=payload, pwd=True, parse=parse)
