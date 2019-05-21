from aiohttp import ClientResponse
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..Session import Session

from ..old_database import SkillDatabase
from ..pattern import PatternManager

results_pattern = PatternManager.getOrCompilePattern("results")


def parse(html: str, **kwargs) -> str:
    match = results_pattern.search(html)

    if match is None:
        return ""

    return match.group(1)


def skill_use(
    session: "Session", skill_id: int, times: int = 1, target: Union[int, str] = None
) -> ClientResponse:
    skill = SkillDatabase.getSkillFromId(skill_id)
    params = {"action": "Skillz", "whichskill": skill["id"]}

    params["bufftimes" if skill["type"] == "Buff" else "quantity"] = times

    if skill["type"] == "Buff":
        params["specificplayer"] = "" if target is None else target
        params["targetplayer"] = session.get_user_id() if target is None else ""

    return session.request("skills.php", pwd=True, params=params, parse=parse)
