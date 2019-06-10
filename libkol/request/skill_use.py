from typing import Union

import libkol

from ..Error import UnknownError
from ..pattern import PatternManager
from ..Skill import Skill
from .request import Request

results_pattern = PatternManager.getOrCompilePattern("results")


class skill_use(Request):
    def __init__(
        self,
        session: "libkol.Session",
        skill: Skill,
        times: int = 1,
        target: Union[int, str] = None,
    ) -> None:
        params = {"action": "Skillz", "whichskill": skill.id}

        params["bufftimes" if skill.buff else "quantity"] = times

        if skill.buff:
            params["specificplayer"] = "" if target is None else target
            params["targetplayer"] = session.get_user_id() if target is None else ""

        self.request = session.request("skills.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> str:
        match = results_pattern.search(content)

        if match is None:
            raise UnknownError("Couldn't parse response from use skill")

        return match.group(1)
