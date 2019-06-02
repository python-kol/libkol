from typing import Union

import pykollib

from .request import Request


class clan_whitelist_remove(Request):
    def __init__(self, session: "pykollib.Session", user: Union[int, str]) -> None:
        payload = {"action": "updatewl", "who": user, "remove": "Remove"}
        self.request = session.request("clan_whitelist.php", data=payload, pwd=True)

    @staticmethod
    async def parser(html: str, **kwargs) -> bool:
        return "<td>Whitelist updated.</td>" in html
