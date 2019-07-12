import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup

import libkol

from ..Error import UnknownError
from .request import Request
from ..util import parsing

username_pattern = re.compile(
    r"<td valign=\"?center\"?>(?:<center>)?(?:<span [^>]+>)?<b>([^<>]+)<\/b> \(#[0-9]+\)<br>"
)
clan_pattern = re.compile(
    r"Clan: <b><a class=nounder href=\"showclan\.php\?whichclan=([0-9]+)\">(.*?)<\/a>"
)


@dataclass
class Profile:
    username: str
    ascensions: Optional[int]
    trophies: Optional[List["libkol.Trophy"]]
    tattoo: Optional[str]
    tattoos: Optional[int]
    clan: Optional["libkol.Clan"]


class player_profile(Request[Profile]):
    def __init__(self, session: "libkol.Session", player_id: int) -> None:
        super().__init__(session)
        payload = {"who": player_id}
        self.request = session.request("showplayer.php", data=payload)

    @staticmethod
    async def parser(content: str, **kwargs) -> Profile:
        from .. import Clan, Trophy

        username_match = username_pattern.search(content)

        if username_match is None:
            raise UnknownError("Cannot match username")

        soup = BeautifulSoup(content, "html.parser")

        # Ascensions
        ascensions_cell = parsing.get_value(soup, "Ascensions")
        ascensions = int(ascensions_cell.string) if ascensions_cell else None

        # Tattoos
        tattoos_cell = parsing.get_value(soup, "Tattoos Collected")
        tattoos = int(tattoos_cell.string) if tattoos_cell else None

        # Tattoo
        tattoo = None  # type: Optional[str]
        tatt_link = soup.find("a", href="account_tattoos.php")
        if tatt_link:
            tattoo = tatt_link.img["alt"][8:]

        # Trophies
        trophies = None # Optional[List[Trophy]]
        if soup.find("center", text="Trophies:") is not None:
            trophies = [
                await Trophy.filter(name=t["title"]).first()
                for t in soup.find_all("img", src=lambda u: "/otherimages/trophy/" in u)
            ]

        # Clan
        clan = None  # type: Optional[libkol.Clan]
        clan_match = clan_pattern.search(content)
        if clan_match:
            clan_id = int(clan_match.group(1))
            clan_name = clan_match.group(2)
            clan = Clan(clan_match, id=clan_id, name=clan_name)

        return Profile(
            username=username_match.group(1),
            ascensions=ascensions,
            trophies=trophies,
            tattoo=tattoo,
            tattoos=tattoos,
            clan=clan,
        )
