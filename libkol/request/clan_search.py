import re
from typing import List

import libkol

from .. import Clan
from .request import Request

clan_search_result_pattern = re.compile(
    r"<b><a href=\"showclan\.php\?recruiter=1&whichclan=([0-9]+)\">([^<>]*)</a></b>"
)


class clan_search(Request[List["Clan"]]):
    def __init__(
        self, session: "libkol.Session", query: str, nameonly: bool = True
    ) -> None:
        data = {
            "action": "search",
            "searchstring": query,
            "whichfield": 1 if nameonly else 0,
            "countoper": 0,
            "countqty": 0,
            "furn1": 0,
            "furn2": 0,
            "furn3": 0,
            "furn4": 0,
            "furn5": 0,
            "furn9": 0,
        }

        self.request = session.request("clan_signup.php", data=data)

    @staticmethod
    async def parser(content: str, **kwargs) -> List["Clan"]:
        session = kwargs["session"]  # type: "libkol.Session"
        return [
            Clan(session, id=int(m.group(1)), name=m.group(2))
            for m in clan_search_result_pattern.finditer(content)
        ]
