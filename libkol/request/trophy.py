import libkol
from bs4 import BeautifulSoup
from typing import List

from ..Trophy import Trophy
from .request import Request


class trophy(Request[List[Trophy]]):
    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        self.request = session.request("trophy.php")

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Trophy]:
        soup = BeautifulSoup(content, "html.parser")

        ids = [
            trophy["value"]
            for trophy in soup.find_all("input", attrs={"name": "whichtrophy"})
        ]

        return await Trophy.filter(id__in=ids)
