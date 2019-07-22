import re
from typing import List, Optional, Tuple
from dataclasses import dataclass
from bs4 import BeautifulSoup

import libkol

from ..Error import UnknownError
from .request import Request
from ..util import parsing

user_pattern = re.compile(
    r"<td valign=\"?center\"?>(?:<center>)?(?:<span [^>]+>)?<b>(?P<username>[^<>]+)<\/b> \(#(?P<user_id>[0-9]+)\)<br>"
)
clan_pattern = re.compile(
    r"Clan: <b><a class=nounder href=\"showclan\.php\?whichclan=([0-9]+)\">(.*?)<\/a>"
)


@dataclass
class Profile:
    ascensions: Optional[int]
    clan: Optional["libkol.Clan"]
    skills: Optional[List[Tuple["libkol.Skill", bool]]]
    tattoo: Optional[str]
    tattoos: Optional[int]
    trophies: Optional[List["libkol.Trophy"]]
    username: str
    id: int


class player_profile(Request[Profile]):
    def __init__(self, session: "libkol.Session", player_id: int) -> None:
        super().__init__(session)
        payload = {"who": player_id}
        self.request = session.request("showplayer.php", data=payload)

    @staticmethod
    async def parser(content: str, **kwargs) -> Profile:
        from .. import Clan, Trophy, Skill

        user_match = user_pattern.search(content)

        if user_match is None:
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

        # Skills
        skills = None  # type: Optional[List[Tuple[Skill, bool]]]
        skills_section = soup.find("div", id="pskills")
        if skills_section is not None:
            skills = []
            for s in skills_section.find_all("tr", class_="blahblah"):
                if s.td.a:
                    skill = await Skill[int(s.td.a["onclick"][17:-1])]
                else:
                    text = s.td.get_text()
                    skill_name = text[0 : text.find("(") - 1]
                    skill = await Skill[skill_name]

                hardcore = True if s.td.b else False

                skills += [(skill, hardcore)]

        # Trophies
        trophies = None  # Optional[List[Trophy]]
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
            ascensions=ascensions,
            clan=clan,
            skills=skills,
            tattoo=tattoo,
            tattoos=tattoos,
            trophies=trophies,
            username=user_match.group("username"),
            id=int(user_match.group("user_id")),
        )
