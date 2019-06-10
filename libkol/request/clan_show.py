from typing import Any, Dict

from bs4 import BeautifulSoup
from yarl import URL

import libkol

from .request import Request


class clan_show(Request[Dict[str, Any]]):
    """
    Get information about a clan
    """

    def __init__(self, session: "libkol.Session", id: int):
        params = {"recruiter": 1, "whichclan": id}
        self.request = session.request("showclan.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> Dict[str, Any]:
        soup = BeautifulSoup(content, "html.parser")
        leader_link = soup.find("a")
        return {
            "name": soup.find("td", bgcolor="blue").string,
            "leader": {
                "id": int(URL(str(leader_link["href"])).query["who"]),
                "username": leader_link.string,
            },
            "website": soup.find("a", target="_blank")["href"],
            "credo": soup.find("table", cellpadding=5).get_text()[6:],
        }
