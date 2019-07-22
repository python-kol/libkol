from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

from bs4 import BeautifulSoup
from yarl import URL

import libkol

from .request import Request


class QueryType(Enum):
    StartsWith = 1
    Contains = 2
    Endswith = 3


@dataclass
class Player:
    username: str
    id: int
    level: int
    character_class: str
    clan_id: Optional[int] = None
    clan_name: Optional[str] = None
    fame: Optional[int] = None


class player_search(Request[List[Player]]):
    def __init__(
        self,
        session: "libkol.Session",
        query: str,
        query_type: QueryType = QueryType.StartsWith,
        pvp_only: bool = False,
        hardcore_only: Optional[bool] = None,
        level: int = None,
        fame: int = None,
    ) -> None:
        super().__init__(session)

        data = {
            "searchstring": query,
            "startswith": query_type.value,
            "searching": "Yep.",
            "hardcoreonly": 0
            if hardcore_only is None
            else 1
            if hardcore_only is True
            else 2,
            "searchlevel": level or "",
            "searchranking": fame or "",
        }

        if pvp_only:
            data["pvponly"] = 1

        self.request = session.request("searchplayer.php", data=data)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Player]:
        soup = BeautifulSoup(content, "html.parser")

        table = soup.find("table")

        players = []  # type: List[Player]

        for row in table.find_all("tr"):
            if row.contents[0].b is None:
                break  # No results

            if row.contents[0].b.u is not None:
                continue  # Header

            players += [
                Player(
                    username=row.contents[0].b.string,
                    id=int(row.contents[1].get_text()),
                    level=int(row.contents[2].get_text()),
                    character_class=row.contents[3].get_text(),
                    clan_id=int(
                        URL(str(row.contents[0].contents[4]["href"])).query["whichclan"]
                    )
                    if len(row.contents[0].contents) > 4
                    else None,
                    clan_name=row.contents[0].contents[4].string
                    if len(row.contents[0].contents) > 4
                    else None,
                    fame=int(row.contents[4].get_text())
                    if len(row.contents) > 4
                    else None,
                )
            ]

        return players
