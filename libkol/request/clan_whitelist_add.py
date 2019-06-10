from typing import NamedTuple, Union

import libkol

from .request import Request


class Response(NamedTuple):
    success: bool
    already: bool


class clan_whitelist_add(Request[Response]):
    def __init__(
        self,
        session: "libkol.Session",
        user: Union[int, str],
        rank: int = 0,
        title: str = "",
    ) -> None:
        payload = {"action": "add", "addwho": user, "level": rank, "title": title}
        self.request = session.request("clan_whitelist.php", data=payload, pwd=True)

    @staticmethod
    async def parser(content: str, **kwargs) -> Response:
        success = " added to whitelist.</td>" in content
        already = "<td>That player is already on the whitelist.</td>" in content

        return Response(success or already, already)
