from aiohttp import ClientResponse
from yarl import URL
from bs4 import BeautifulSoup
from typing import Dict, Any, TYPE_CHECKING

from .ClanRaidLogRequest import parse_raid_log

if TYPE_CHECKING:
    from ..Session import Session


def parse(html: str, url: "URL", **kwargs) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")

    raids = soup.find("b", text="Current Clan Dungeons:").next_sibling.find_all("div")

    logs = []
    for d in raids:
        info = list(d.find("b").children)
        name = info[0][:-1].lower()
        id = int(info[1].split(":")[-1])
        logs += [parse_raid_log(name, id, d.find("td"))]

    return logs


async def clanRaidsRequest(session: "Session") -> ClientResponse:
    """
    Retrieves information on all active raids
    """

    return await session.post("clan_raidlogs.php", parse=parse)
