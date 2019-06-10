import re
from enum import Enum
from typing import Dict

import libkol

from .request import Request


class QuestPage(Enum):
    Current = 1
    Completed = 2
    Accomplishments = 3
    Notes = 4
    HoboCode = 5
    MonsterManuel = 6


quests_completed_pattern = re.compile(
    r"<b>([\w\s,\.\'\?!]+)<\/b>(?!<\/td>)<br>([\w\s,\.\'\?!]+)<p>"
)


class questlog(Request):
    """
    Get info from the quest log about which quests are completed and which stage of each uncompleted quest the player is on

    :param page: Page of the quest log to request
    """

    def __init__(
        self, session: "libkol.Session", page: QuestPage = QuestPage.Current
    ) -> None:
        params = {"which": page.value}
        self.request = session.request("questlog.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> Dict[str, str]:
        return {
            match.group(1): match.group(2)
            for match in quests_completed_pattern.finditer(content)
        }
