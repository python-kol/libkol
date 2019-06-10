import re
from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass

from bs4 import BeautifulSoup

import libkol

from .request import Request


@dataclass
class Ascension:
    """
    Ascension
    """

    id: int  # The ascension id
    dropped_path: bool  # Whether the path was dropped in-run
    level: int  # The level at which the user broke the prism
    player_class: str  # The class the player was during the ascension
    moon: str  # The moonsign of the ascension
    turns: int  # The total number of turns the ascension lasted
    familiar: Optional[
        str
    ]  # The most used familiar in-run this ascension, or None if there was no familiar
    familiar_percentage: Optional[
        float
    ]  # The percentage of turns the most used familiar in-run was used
    total_familiar: Optional[str]  # The most used familiar overall this ascension
    total_familiar_percentage: Optional[
        float
    ]  # The percentage of turns the most used familiar overall was used
    restriction: str  # The restriction in place for this ascension (hardcore, normal, casual etc)
    path: Optional[
        str
    ]  # The path in place for this ascension (teetolar, oxygenarian, Avatar of Jarlsberg etc)
    start: datetime  # The start date of the run
    end: datetime  # The end date of the run


def get_int_cell(c: BeautifulSoup) -> int:
    return int((c.span if c.span else c).string.replace(",", ""))


familiar_pattern = re.compile(
    r"^(.*?) \(([0-9]+(?:\.[0-9]+)?)%\)(?: - Total Run: (.*?) \(([0-9]+(?:\.[0-9]+)?)%\))?"
)


class ascension_history(Request[List[Ascension]]):
    """
    Fetches ascension history for a player

    :params player_id: Player for whom to fetch ascension history
    :params pre_ns13: Whether to include pre NS13 ascension history
    """

    def __init__(
        self, session: "libkol.Session", player_id: int, pre_ns13: bool = False
    ) -> None:
        params = {"back": "other", "who": player_id, "prens13": 1 if pre_ns13 else 0}
        self.request = session.request("ascensionhistory.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Ascension]:
        """
        Parses through the response and constructs an array of ascensions.
        """
        soup = BeautifulSoup(content, "html.parser")
        end_dates = soup.find_all("td", height="30")

        ascensions = []  # type: List[Ascension]

        for end in end_dates:
            id = end.previous_sibling
            level, cl, moon, turns, days, familiar, info = end.find_next_siblings("td")[
                0:7
            ]

            info = info.find_all("img")

            path = None if len(info) < 2 else info[1]["title"]
            if path and path.endswith(")"):
                path = path[0 : path.find("(") - 1]

            id_string = id.string.strip()
            end_date = datetime.strptime(end.string.strip(), "%m/%d/%y")
            fam_data = familiar.img["alt"] if familiar.img else None
            fam_match = None if fam_data is None else familiar_pattern.match(fam_data)

            ascensions += [
                Ascension(
                    id=int(id_string.strip("*")),
                    dropped_path=id_string.endswith("*"),
                    level=int(level.span.string),
                    player_class=cl.img["alt"],
                    moon=moon.string.strip().lower(),
                    turns=get_int_cell(turns),
                    familiar=None if fam_match is None else fam_match.group(1),
                    familiar_percentage=(
                        None if fam_match is None else float(fam_match.group(2))
                    ),
                    total_familiar=None if fam_match is None else fam_match.group(3),
                    total_familiar_percentage=(
                        None
                        if fam_match is None or fam_match.group(4) is None
                        else float(fam_match.group(4))
                    ),
                    restriction=(
                        info[0]["title"].lower() if info[0].has_attr("title") else None
                    ),
                    path=path,
                    start=end_date - timedelta(days=get_int_cell(days)),
                    end=end_date,
                )
            ]

        return ascensions
