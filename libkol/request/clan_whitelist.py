import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup

import libkol

from .request import Request

rank_pattern = re.compile(r"(.*?) \(°([0-9]+)\)")


class clan_whitelist(Request[List[Dict[str, Any]]]):
    """
    Retrieves information from the clan whitelist page.
    """

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        self.request = session.request("clan_whitelist.php")

    @staticmethod
    async def parser(
        content: str, include_rank: bool = False, only_rank: bool = False, **kwargs
    ) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(content, "html.parser")

        # Get rid of stupid forms everywhere
        for f in soup.find_all("form"):
            f.unwrap()

        # If we want to include the ranks of the whitelist we can, but it's off by default
        if include_rank or only_rank:
            ranks = [
                {"id": id, "name": name, "number": number}
                for id, name, number in (
                    (int(o["value"]), *rank_matcher.groups())
                    for o, rank_matcher in (
                        (o, rank_pattern.match(o.string))
                        for o in soup.find(
                            "select",
                            attrs={"name": lambda n: n and n.startswith("level")},
                        ).children
                    )
                    if rank_matcher is not None
                )
            ]

        if only_rank:
            return ranks

        members = [
            {
                "username": cells[0].a.b.string,
                "user_id": cells[0].input["value"],
                "rank": next(
                    (
                        rank
                        for rank in ranks
                        if (
                            rank["id"]
                            == int(
                                cells[1]
                                .find("select")
                                .find("option", selected=True)["value"]
                            )
                            if cells[1].find("select")
                            else rank["name"] == cells[1].string
                        )
                    ),
                    None,
                )
                if include_rank
                else None,
            }
            for cells in (
                row.find_all("td")
                for table in [
                    soup.find("b", text="People In Your Clan"),
                    soup.find("b", text="People Not In Your Clan"),
                ]
                for row in table.find_parent("tr").find_next_siblings("tr")[1:]
            )
        ]

        return members
