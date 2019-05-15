import re
from bs4 import BeautifulSoup
from aiohttp import ClientResponse
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..Session import Session

rankNameAndNumber = re.compile(r"(.*?) \(°([0-9]+)\)")


def parse(html: str, include_rank: bool = False, only_rank: bool = False, **kwargs):
    soup = BeautifulSoup(html, "html.parser")

    # Get rid of stupid forms everywhere
    for f in soup.find_all("form"):
        f.unwrap()

    # If we want to include the ranks of the whitelist we can, but it's off by default
    if include_rank or only_rank:
        ranks = [
            {"id": id, "name": name, "number": number}
            for id, name, number in (
                (int(o["value"]), *rankNameAndNumber.match(o.string).groups())
                for o in soup.find(
                    "select", attrs={"name": lambda n: n and n.startswith("level")}
                ).children
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


def clanWhitelistRequest(session: "Session") -> ClientResponse:
    "Retrieves information from the clan whitelist page."

    return session.request("clan_whitelist.php", parse=parse)
