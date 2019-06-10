from typing import Union

import libkol

from .request import Request


class clan_whitelist_remove(Request[bool]):
    def __init__(self, session: "libkol.Session", user: Union[int, str]) -> None:
        payload = {"action": "updatewl", "who": user, "remove": "Remove"}
        self.request = session.request("clan_whitelist.php", data=payload, pwd=True)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        return "<td>Whitelist updated.</td>" in content
