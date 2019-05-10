from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, Any, TYPE_CHECKING
from urllib.parse import urlparse, parse_qs
import re

from ..Error import ClanRaidsNotFoundError

if TYPE_CHECKING:
    from ..Session import Session

pageSummary = re.compile(r"Showing [0-9]+-[0-9]+ of ([0-9]+)")
notFound = re.compile(r"\(No previous Clan Dungeon records found\)")


def parse(html: str, **kwargs) -> Dict[str, Any]:
    if notFound.search(html):
        raise ClanRaidsNotFoundError("Page of old clan raids not found")

    soup = BeautifulSoup(html, "html.parser")
    summary = soup.find(text=pageSummary)
    total = int(pageSummary.search(summary).group(1))
    rows = soup.find_all("tr")[2:]

    raids = []
    for r in rows:
        cells = r.find_all("td")
        start = datetime.strptime(
            cells[0].text.replace(u"\xa0", ""), "%B %d, %Y"
        ).date()
        end = datetime.strptime(cells[1].text.replace(u"\xa0", ""), "%B %d, %Y").date()
        name = cells[2].text.replace(u"\xa0", "").lower()
        url = cells[4].find("a")["href"]
        id = int(parse_qs(urlparse(url).query)["viewlog"][0])
        raids.append({"id": id, "name": name, "start": start, "end": end})

    return {"total": total, "raids": raids}


def clanRaidsPreviousRequest(session: "Session", page: int = 0) -> ClientResponse:
    """
    Retrieves a list of old raid logs, in pages of length 10
    """
    params = {"startrow": page * 10}

    return session.request("clan_oldraidlogs.php", params=params, parse=parse)
