import re
from typing import List

from yarl import URL

import pykollib

from .. import Clan
from .request import Request

clan_search_result_pattern = re.compile(
    r"<b><a href=\"showclan\.php\?recruiter=1&whichclan=([0-9]+)\">([^<>]*)</a></b>"
)


class clan_search(Request):
    def __init__(
        self, session: "pykollib.Session", query: str, nameonly: bool = True
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
    def parser(
        html: str, url: URL, session: "pykollib.Session", **kwargs
    ) -> List["Clan"]:
        return [
            Clan(session, id=int(m.group(1)), name=m.group(2))
            for m in clan_search_result_pattern.finditer(html)
        ]
