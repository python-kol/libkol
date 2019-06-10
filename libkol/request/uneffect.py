import libkol

from ..Error import EffectNotFoundError, ItemNotFoundError, UnknownError
from .request import Request


class uneffect(Request[bool]):
    def __init__(self, session: "libkol.Session", effect_id: int) -> None:
        super().__init__(session)
        params = {"using": "Yep.", "whicheffect": effect_id}

        self.request = session.request("uneffect.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        if "<td>You don't have that effect." in content:
            raise EffectNotFoundError(
                "Unable to remove effect. The user does not have that effect."
            )

        if "<td>You don't have a green soft eyedrop echo antidote." in content:
            raise ItemNotFoundError(
                "Unable to remove effect. You do not have a soft green echo eyedrop antidote."
            )

        if "<td>Effect removed.</td>" not in content:
            raise UnknownError("Unable to remove effect")

        return True
