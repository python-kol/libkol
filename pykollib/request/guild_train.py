from .request import Request

import pykollib

from ..Error import (AlreadyCompletedError, NotEnoughMeatError,
                     SkillNotFoundError, UnknownError, UserIsLowLevelError)
from ..Skill import Skill

class guild_train(Request):
    def __init__(self, session: "pykollib.Session", skill: Skill) -> None:
        super().__init__(session)
        data = {"action": "train", "whichskill": skill.id}

        self.request = session.request("guild.php", pwd=True, data=data)

    @staticmethod
    def parser(html: str, **kwargs) -> bool:
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
