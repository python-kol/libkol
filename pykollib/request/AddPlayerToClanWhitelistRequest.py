from aiohttp import ClientResponse
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..Session import Session


def parse(html: str, **kwargs):
    print(html)
    if html.index("That player is already on the whitelist."):
        return True


def addPlayerToClanWhitelistRequest(
    session: "Session", user: Union[int, str], rank: int = 0, title: str = ""
) -> ClientResponse:
    payload = {"action": "add", "addwho": user, "level": rank, "title": title}

    return session.request("clan_whitelist.php", data=payload, pwd=True, parse=parse)
