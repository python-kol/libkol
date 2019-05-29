from aiohttp import ClientResponse
from typing import TYPE_CHECKING, Any, Coroutine

if TYPE_CHECKING:
    from ..Session import Session

from ..Error import (
    UserIsLowLevelError,
    SkillNotFoundError,
    NotEnoughMeatError,
    AlreadyCompletedError,
    UnknownError,
)
from ..Skill import Skill


def parse(html: str, **kwargs: Any) -> bool:
    if ">You're not powerful enough to train that skill.<" in html:
        raise UserIsLowLevelError("You aren't a high enough level to learn that skill.")

    if ">Invalid skill selected.<" in html:
        raise SkillNotFoundError("You cannot train that skill at the Guild Hall.")

    if ">You can't afford to train that skill.<" in html:
        raise NotEnoughMeatError("You cannot afford to train that skill")

    if ">You've already got that skill.<" in html:
        raise AlreadyCompletedError("You already know that skill.")

    if ">You learn a new skill: <b>" not in html:
        raise UnknownError("Unknown error")

    return True


def guild_train(
    session: "Session", skill: Skill
) -> Coroutine[Any, Any, ClientResponse]:
    data = {"action": "train", "whichskill": skill.id}

    return session.request("guild.php", pwd=True, data=data, parse=parse)
