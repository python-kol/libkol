from typing import Any, Coroutine, NamedTuple, Union

from aiohttp import ClientResponse

import pykollib


class Response(NamedTuple):
    success: bool
    already: bool


def parse(html: str, **kwargs) -> Response:
    success = " added to whitelist.</td>" in html
    already = "<td>That player is already on the whitelist.</td>" in html

    return Response(success or already, already)


def clan_whitelist_add(
    session: "pykollib.Session", user: Union[int, str], rank: int = 0, title: str = ""
) -> Coroutine[Any, Any, ClientResponse]:
    payload = {"action": "add", "addwho": user, "level": rank, "title": title}
    return session.request("clan_whitelist.php", data=payload, pwd=True, parse=parse)
