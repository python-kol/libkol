from bs4 import BeautifulSoup
from enum import Enum
from aiohttp import ClientResponse
from yarl import URL
from typing import TYPE_CHECKING, Coroutine, Any, Optional, NamedTuple, List

if TYPE_CHECKING:
    from ..Session import Session


class QueryType(Enum):
    StartsWith = 1
    Contains = 2
    Endswith = 3


class Result(NamedTuple):
    username: str
    user_id: int
    level: int
    character_class: str
    clan_id: Optional[int] = None
    clan_name: Optional[str] = None
    fame: Optional[int] = None


def parse(html: str, **kwargs) -> List[Result]:
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")

    players = []  # type: List[Result]

    for row in table.find_all("tr"):
        if row.contents[0].b.u is not None:
            continue  # Header

        players += [
            Result(
                row.contents[0].b.string,
                int(row.contents[1].get_text()),
                int(row.contents[2].get_text()),
                row.contents[3].get_text(),
                int(URL(row.contents[0].contents[4]["href"]).query["whichclan"])
                if len(row.contents[0].contents) > 4
                else None,
                row.contents[0].contents[4].string
                if len(row.contents[0].contents) > 4
                else None,
                int(row.contents[4].get_text()) if len(row.contents) > 4 else None,
            )
        ]

    return players


def player_search(
    session: "Session",
    query: str,
    query_type: QueryType = QueryType.StartsWith,
    pvp_only: bool = False,
    hardcore_only: Optional[bool] = None,
    level: int = 0,
    fame: int = 0,
) -> Coroutine[Any, Any, ClientResponse]:
    data = {
        "searchstring": query,
        "startswith": query_type,
        "searching": "Yep",
        "pvponly": 1 if pvp_only else 0,
        "hardcoreonly": 0
        if hardcore_only is None
        else 1
        if hardcore_only is True
        else 2,
        "searchlevel": level,
        "searchranking": fame,
    }
    return session.request("searchplayer.php", data=data, parse=parse)
