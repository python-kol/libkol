from typing import Any, Coroutine, Union

from aiohttp import ClientResponse

import pykollib


def parse(html: str, **kwargs) -> bool:
    return "<td>Whitelist updated.</td>" in html


def clan_whitelist_remove(session: "pykollib.Session", user: Union[int, str]) -> Coroutine[Any, Any, ClientResponse]:
    payload = {"action": "updatewl", "who": user, "remove": "Remove"}
    return session.request("clan_whitelist.php", data=payload, pwd=True, parse=parse)
