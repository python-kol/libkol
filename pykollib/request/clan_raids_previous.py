import re
from datetime import date, datetime
from typing import Any, Dict, List, NamedTuple

from bs4 import BeautifulSoup
from yarl import URL

import pykollib

from ..Error import ClanRaidsNotFoundError, UnknownError
from .request import Request

summary_pattern = re.compile(r"Showing [0-9]+-[0-9]+ of ([0-9]+)")


class Raid(NamedTuple):
    id: int
    name: str
    start: date
    end: date


class Response(NamedTuple):
    total: int
    raids: List[Raid]

class clan_raids_previous(Request):
    """
    Retrieves a list of old raid logs, in pages of length 10
    """
    def __init__(self, session: "pykollib.Session", page: int = 0) -> None:

        super().__init__(session)
        params = {"startrow": page * 10}

        self.request = session.request("clan_oldraidlogs.php", params=params)

    @staticmethod
    async def parser(html: str, url: URL, **kwargs) -> Response:
        if "(No previous Clan Dungeon records found)" in html:
            raise ClanRaidsNotFoundError("Page of old clan raids not found")

        soup = BeautifulSoup(html, "html.parser")
        summary = soup.find(text=summary_pattern)
        m = summary_pattern.search(summary.string)

        if m is None:
            raise UnknownError("Cannot parse clan raid summary")

        total = int(m.group(1))
        rows = soup.find_all("tr")[2:]

        raids = []
        for r in rows:
            cells = r.find_all("td")
            start = datetime.strptime(
                cells[0].text.replace(u"\xa0", ""), "%B %d, %Y"
            ).date()
            end = datetime.strptime(
                cells[1].text.replace(u"\xa0", ""), "%B %d, %Y"
            ).date()
            name = cells[2].text.replace(u"\xa0", "").lower()
            page_url = URL(str(cells[4].find("a")["href"]))
            id = int(page_url.query["viewlog"])
            raids.append(Raid(id=id, name=name, start=start, end=end))

        return Response(total=total, raids=raids)
