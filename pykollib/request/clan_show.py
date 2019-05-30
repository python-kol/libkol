from typing import Any, Coroutine, Dict

from bs4 import BeautifulSoup
from yarl import URL

import pykollib


def parse(html: str, **kwargs) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    leader_link = soup.find("a")
    return {
        "name": soup.find("td", bgcolor="blue").string,
        "leader": {
            "id": int(URL(leader_link["href"]).query["who"]),
            "username": leader_link.string,
        },
        "website": soup.find("a", target="_blank")["href"],
        "credo": soup.find("table", cellpadding=5).get_text()[6:],
    }


def clan_show(session: "pykollib.Session", id: int):
    "Get information about a clan"

    params = {"recruiter": 1, "whichclan": id}
    return session.request("showclan.php", parse=parse, params=params)
