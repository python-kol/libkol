from aiohttp import ClientResponse
from yarl import URL
from bs4 import BeautifulSoup, PageElement
from typing import Tuple, Dict, List, Any, TYPE_CHECKING

from ..Error import ClanPermissionsError
from .ClanRaidLogRequest import parse_raid_log

if TYPE_CHECKING:
    from ..Session import Session


def dungeon_name_id_from_title(comment: List[PageElement]) -> Tuple[str, int]:
    return (comment[0][:-1].lower(), int(comment[1].split(":")[-1]))


def parse(html: str, url: URL, **kwargs) -> Dict[str, Any]:
    if (
        "Your clan has a basement, but you are not allowed to enter clan dungeons, "
        "so this is as far as you're going, Gilbert."
    ) in html or html == "":
        raise ClanPermissionsError("You do not have dungeon access for this clan")

    soup = BeautifulSoup(html, "html.parser")
    raids = soup.find("b", text="Current Clan Dungeons:").next_sibling.find_all("div")
    return [
        parse_raid_log(*dungeon_name_id_from_title(d.find("b").contents), d.find("td"))
        for d in raids
    ]


def clanRaidsRequest(session: "Session") -> ClientResponse:
    """
    Retrieves information on all active raids
    """

    return session.request("clan_raidlogs.php", parse=parse)
