import libkol

from ..Error import (
    AlreadyCompletedError,
    NotEnoughMeatError,
    SkillNotFoundError,
    UnknownError,
    UserIsLowLevelError,
)
from ..Skill import Skill
from .request import Request


class guild_train(Request):
    def __init__(self, session: "libkol.Session", skill: Skill) -> None:
        super().__init__(session)
        data = {"action": "train", "whichskill": skill.id}

        self.request = session.request("guild.php", pwd=True, data=data)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        if ">You're not powerful enough to train that skill.<" in content:
            raise UserIsLowLevelError(
                "You aren't a high enough level to learn that skill."
            )

        if ">Invalid skill selected.<" in content:
            raise SkillNotFoundError("You cannot train that skill at the Guild Hall.")

        if ">You can't afford to train that skill.<" in content:
            raise NotEnoughMeatError("You cannot afford to train that skill")

        if ">You've already got that skill.<" in content:
            raise AlreadyCompletedError("You already know that skill.")

        if ">You learn a new skill: <b>" not in content:
            raise UnknownError("Unknown error")

        return True
