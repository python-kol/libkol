from typing import Any, Dict, List, Tuple

from bs4 import BeautifulSoup, Tag
from yarl import URL

import pykollib

from ..Error import ClanPermissionsError
from .clan_raid_log import clan_raid_log
from .request import Request


class clan_raids(Request):
    """
    Retrieves information on all active raids
    """
    def __init__(self, session: "pykollib.Session") -> None:
        super().__init__(session)

        self.request = session.request("clan_raidlogs.php")

    @staticmethod
    def dungeon_name_id_from_title(comment: List[Tag]) -> Tuple[str, int]:
        return (comment[0].string[:-1].lower(), int(comment[1].string.split(":")[-1]))

    @classmethod
    async def parser(cls, html: str, url: URL, **kwargs) -> List[Dict[str, Any]]:
        if (
            "Your clan has a basement, but you are not allowed to enter clan dungeons, "
            "so this is as far as you're going, Gilbert."
        ) in html or html == "":
            raise ClanPermissionsError("You do not have dungeon access for this clan")

        soup = BeautifulSoup(html, "html.parser")

        current = soup.find("b", text="Current Clan Dungeons:")

        if current is None:
            raise ClanPermissionsError("You cannot see any current clan dungeons")

        raids = current.next_sibling.find_all("div")
        return [
            clan_raid_log.parse_raid_log(
                *cls.dungeon_name_id_from_title(d.find("b").contents), d.find("td")
            )
            for d in raids
        ]
