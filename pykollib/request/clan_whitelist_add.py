from typing import NamedTuple, Union

import pykollib

from .request import Request


class Response(NamedTuple):
    success: bool
    already: bool


class clan_whitelist_add(Request):
    def __init__(
        self,
        session: "pykollib.Session",
        user: Union[int, str],
        rank: int = 0,
        title: str = "",
    ) -> None:
        payload = {"action": "add", "addwho": user, "level": rank, "title": title}
        self.request = session.request("clan_whitelist.php", data=payload, pwd=True)

    @staticmethod
    async def parser(html: str, **kwargs) -> Response:
        success = " added to whitelist.</td>" in html
        already = "<td>That player is already on the whitelist.</td>" in html

        return Response(success or already, already)
