from typing import Optional

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
        target: Optional[int] = None,
    ) -> None:
        super().__init__(session)
        params = {"action": "Skillz", "whichskill": skill.id}

        params["quantity"] = times

        if skill.buff:
            params["targetplayer"] = session.user_id if target is None else target

        self.request = session.request(
            "runskillz.php", ajax=True, pwd=True, params=params
        )

    @staticmethod
    async def parser(content: str, **kwargs) -> str:
        match = results_pattern.search(content)

        if match is None:
            raise UnknownError("Couldn't parse response from use skill")

        return match.group(1)
