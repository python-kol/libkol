import asyncio
from typing import List
from bs4 import BeautifulSoup

import libkol

from ..Skill import Skill
from .request import Request


class skills(Request[List[Skill]]):
    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        params = {"layout": 1}
        self.request = session.request("skillz.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Skill]:
        session = kwargs["session"]  # type: "libkol.Session"

        soup = BeautifulSoup(content, "html.parser")

        tasks = [Skill[int(box["rel"])] for box in soup.find_all("div", class_="skill")]
        knowledge = await asyncio.gather(*tasks)

        session.state["skills"] = knowledge
        return knowledge
